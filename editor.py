import sys
import pygame
from script.utils import load_image, load_images, Animation
from script.tilemap import Tilemap

RENDER_SCALE_X = 3.29375
RENDER_SCALE_Y = 2.13

class Editor:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('editor')
        self.screen = pygame.display.set_mode((1054, 512))
        self.display = pygame.Surface((320, 240))
        self.clock = pygame.time.Clock()
        self.collected_stars = set()
        
        # cargar assets
        self.assets = {
            'caja': load_images('Tiles/caja', (16,16)),
            'piso': load_images('Tiles/pisos', (16,16)), 
            'silla': load_images('Tiles/silla', (8,6)),
            'barrier' : load_images('Tiles/barrier'),
            'obama' : load_images('Obama_PJ'),
            'obamacolgado' : load_images('Obama_PJ'),
            'kimyputin' : load_images('Obama_PJ'),
            'laser' : load_images('Tiles/laser'),
            'soga' : load_images('Tiles/laser'),
            'barril' : load_images('Tiles/barbarril'),
            'estrella' : load_images('Tiles/estrella'),
            'people' : load_images('Tiles/personas'),
            'elmatador' : load_images('Tiles/elmatador'),
            'pisos variables' : load_images('Tiles/pisos variables'),
            'carteles' : load_images('Tiles/textos'),
            'sign' : load_images('Tiles/cartel'),
        }

        self.movement = [False, False, False, False]

        self.tilemap = Tilemap(self, tile_size=16)

        try: 
            self.tilemap.load("1.json")

        except FileNotFoundError:
            pass
        
        self.scroll = [0, 0]
        
        self.tile_list = list(self.assets)
        self.tile_group = 0
        self.tile_variant = 0

        self.clicking = False
        self.right_clicking = False
        self.shift = False
        self.ongrid = True


    def run(self):
        # arranque
        while True:
            self.display.fill ((255,255, 255))  # fondo 

            self.scroll[0] += (self.movement[1] - self.movement[0]) * 2
            self.scroll[1] += (self.movement[3] - self.movement[2]) * 2

            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.tilemap.render (self.display, offset=render_scroll)

            current_tile_img = self.assets[self.tile_list[self.tile_group]][self.tile_variant].copy()
            current_tile_img.set_alpha (100)

            mpos = pygame.mouse.get_pos() 
            mpos = (mpos[0] / RENDER_SCALE_X, mpos[1] / RENDER_SCALE_Y)

            tile_pos = (int((mpos[0] + self.scroll[0]) // self.tilemap.tile_size), int((mpos[1] + self.scroll [1]) / self.tilemap.tile_size))

            if self.ongrid :
                self.display.blit(current_tile_img, (tile_pos[0] * self.tilemap.tile_size - self.scroll[0], tile_pos[1] * self.tilemap.tile_size - self.scroll[1]))
            else:
                self.display.blit(current_tile_img, mpos)  
            
            if self.clicking and self.ongrid :
                self.tilemap.tilemap [str(tile_pos[0]) + ';' + str(tile_pos[1])] = {"type" : self.tile_list[self.tile_group], "variant" : self.tile_variant, "pos" : tile_pos}
            if self.right_clicking :
                tile_loc = str(tile_pos[0]) + ';' + str(tile_pos[1])
                if tile_loc in self.tilemap.tilemap :
                    del self.tilemap.tilemap[tile_loc]
                for tile in self.tilemap.offgrid_tiles.copy() :
                    tile_img = self.assets[tile["type"]][tile["variant"]]
                    tile_r = pygame.Rect(tile["pos"][0] - self.scroll[0], tile["pos"][1] - self.scroll[1], tile_img.get_width(), tile_img.get_height())
                    if tile_r.collidepoint (mpos) :
                        self.tilemap.offgrid_tiles.remove(tile)


            self.display.blit(current_tile_img, (5, 5))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit() # para salir
                if event.type == pygame.MOUSEBUTTONDOWN :
                    if event.button == 1 :
                        self.clicking = True
                        if not self.ongrid :
                            self.tilemap.offgrid_tiles.append({"type" : self.tile_list[self.tile_group], "variant" : self.tile_variant, "pos" : (mpos[0] + self.scroll[0], mpos[1] + self.scroll[1])})
                    if event.button == 3 :
                        self.right_clicking = True
                    if self.shift :
                        if event.button == 4 :
                            self.tile_variant = (self.tile_variant - 1) % len (self.assets[self.tile_list[self.tile_group]])
                        if event.button == 5 :
                            self.tile_variant = (self.tile_variant + 1) % len (self.assets[self.tile_list[self.tile_group]])
                    else :
                        if event.button == 4 :
                            self.tile_group = (self.tile_group - 1) % len (self.tile_list)
                            self.tile_variant = 0
                        if event.button == 5 :
                            self.tile_group = (self.tile_group + 1) % len (self.tile_list)
                            self.tile_variant = 0
                if event.type == pygame.MOUSEBUTTONUP :
                    if event.button == 1 :
                        self.clicking = False 
                    if event.button == 3 :
                        self.right_clicking = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.movement[1] = True
                    if event.key == pygame.K_UP or event.key == pygame.K_w :
                        self.movement [2] = True
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s :
                        self.movement [3] = True
                    if event.key == pygame.K_LSHIFT :
                        self.shift = True
                    if event.key == pygame.K_g :
                        self.ongrid = not self.ongrid
                    if event.key == pygame.K_t :
                        self.tilemap.autotile()
                    if event.key == pygame.K_o :
                        self.tilemap.save('maps/1.json')



                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.movement[1] = False
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.movement [2] = False
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s :
                        self.movement [3] = False
                    if event.key == pygame.K_LSHIFT :
                        self.shift = False            
        
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0)) # escalar a pantalla
            pygame.display.update()
            self.clock.tick(60)

Editor().run()