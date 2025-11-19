import pygame, json

AUTOTILES_MAP = {
    tuple(sorted([(1, 0), (0, 1)])): 0,
    tuple(sorted([(1, 0), (0, 1), (-1, 0)])): 1,
    tuple(sorted([(-1, 0), (0, 1)])): 2, 
    tuple(sorted([(-1, 0), (0, -1), (0, 1)])): 3,
    tuple(sorted([(-1, 0), (0, -1)])): 4,
    tuple(sorted([(-1, 0), (0, -1), (1, 0)])): 5,
    tuple(sorted([(1, 0), (0, -1)])): 6,
    tuple(sorted([(1, 0), (0, -1), (0, 1)])): 7,
    tuple(sorted([(1, 0), (-1, 0), (0, 1), (0, -1)])): 8,
    
}

NEIGHBOR_OFFSETS = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 0), (-1, 1), (0, 1), (1, 1)] # offsets para tiles vecinos
PHYSICS_TILES = {'piso', 'caja', 'barrier','barril','pisos variables',"people",} # que tiles tienen colision
AUTOTILES_TYPES = {'piso'}

class Tilemap:
    

    def __init__(self, game, tile_size=16):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}
        self.offgrid_tiles = []


    def tiles_around(self, pos):
        tiles = []
        tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        for offset in NEIGHBOR_OFFSETS:
            check_loc = str(tile_loc[0] + offset[0]) + ';' + str(tile_loc[1] + offset[1])
            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])
        return tiles
        # detecta las 9 tiles alredor del pj

    def save(self, path) :
        f = open(path, "w")
        json.dump({"tilemap" : self.tilemap, "tile_size" : self.tile_size, "offgrid" : self.offgrid_tiles}, f)
        f.close()

    def load (self, path) :
        BASE_FOLDER_PATH = "maps/"
        f = open(BASE_FOLDER_PATH + path, "r")
        map_data = json.load (f)
        f.close()
    
        self.tilemap = map_data['tilemap']
        self.tile_size = map_data['tile_size']
        self.offgrid_tiles = map_data['offgrid']

    def physics_rects_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos):
            if tile['type'] in PHYSICS_TILES:
                rects.append(pygame.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size))
        return rects
        # detecta cuales de esas 9 tiles tiene colisiones

    def check_obama_collision(self, player_rect):
        for tile in self.tiles_around((player_rect.centerx, player_rect.centery)):
            if tile['type'] == 'obama' or tile['type'] == 'obamacolgado'or tile['type'] == 'kimyputin':
                obama_rect = pygame.Rect(
                    tile['pos'][0] * self.tile_size, 
                    tile['pos'][1] * self.tile_size, 
                    self.tile_size, 
                    self.tile_size
                )
                if player_rect.colliderect(obama_rect):
                    return True
        return False

    def check_spikes_collision(self, player_rect):
        for tile in self.tiles_around((player_rect.centerx, player_rect.centery)):
            if tile['type'] == 'elmatador':
                elmatador_rect = pygame.Rect(
                    tile['pos'][0] * self.tile_size, 
                    tile['pos'][1] * self.tile_size, 
                    self.tile_size, 
                    self.tile_size
                )
                if player_rect.colliderect(elmatador_rect):
                    return True
        return False

    def check_chair_collision(self, player_rect):
        for tile in self.tiles_around((player_rect.centerx, player_rect.centery)):
            if tile['type'] == 'silla':
                chair_rect = pygame.Rect(
                    tile['pos'][0] * self.tile_size, 
                    tile['pos'][1] * self.tile_size, 
                    self.tile_size, 
                    self.tile_size
                )
                if player_rect.colliderect(chair_rect):
                    return True
        return False

    def check_sign_collision(self, player_rect):
        for tile in self.tiles_around((player_rect.centerx, player_rect.centery)):
            if tile['type'] == 'cartel':
                sign_rect = pygame.Rect(
                    tile['pos'][0] * self.tile_size, 
                    tile['pos'][1] * self.tile_size, 
                    self.tile_size, 
                    self.tile_size
                )
                if player_rect.colliderect(sign_rect):
                    return True
        return False

    def check_star_collision(self, player_rect):
        for tile in self.tiles_around((player_rect.centerx, player_rect.centery)):
            if tile['type'] == 'estrella':
                tile_loc = str(tile['pos'][0]) + ';' + str(tile['pos'][1])
                
                # Si ya fue recolectada, no hacer nada
                if tile_loc in self.game.collected_stars:
                    continue
                    
                estrella_rect = pygame.Rect(
                    tile['pos'][0] * self.tile_size, 
                    tile['pos'][1] * self.tile_size, 
                    self.tile_size, 
                    self.tile_size
                )
                if player_rect.colliderect(estrella_rect):
                    return tile_loc  # devuelve la ubicación en lugar de True
        return None

    def autotile (self) :
        for loc in self.tilemap :
            tile = self.tilemap [loc]
            neighbors =  set()
            for shift in [(1,0), (-1,0), (0,1), (0,-1)] :
                check_loc = str(tile['pos'][0] + shift[0]) + ';' + str(tile['pos'][1] + shift[1])
                if check_loc in self.tilemap :
                    if self.tilemap[check_loc]['type'] == tile['type'] :
                        neighbors.add(shift)
            neighbors = tuple(sorted(neighbors))
            if (tile['type'] in AUTOTILES_TYPES) and (neighbors in AUTOTILES_MAP) :
                tile['variant'] = AUTOTILES_MAP[neighbors]


    def render(self, surf, offset = (0,0)):
        for tile in self.offgrid_tiles:
            surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1]))
        # carga las futuras decoraciones y objetos sin colisiones
        for x in range(int(offset[0] // self.tile_size), int((offset[0] + surf.get_width()) // self.tile_size) + 1):
            for y in range(int(offset[1] // self.tile_size), int((offset[1] + surf.get_height()) // self.tile_size) + 1):
                loc = str(x) + ';' + str(y)
                if loc in self.tilemap:
                    tile = self.tilemap[loc]
                    if tile['type'] == 'estrella' and loc in self.game.collected_stars:
                        surf.blit(self.game.assets[tile['type']][1], 
                                (tile['pos'][0] * self.tile_size - offset[0], 
                                tile['pos'][1] * self.tile_size - offset[1]))
                    else:
                        surf.blit(self.game.assets[tile['type']][tile['variant']], 
                                (tile['pos'][0] * self.tile_size - offset[0], 
                                tile['pos'][1] * self.tile_size - offset[1]))
            