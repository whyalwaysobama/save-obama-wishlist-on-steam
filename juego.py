import sys
import pygame
from script.utils import load_image, load_images, Animation
from script.entitites import PhysicsEntity, Player
from script.tilemap import Tilemap
from script.menu import Menu

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Save Obama')
        self.screen = pygame.display.set_mode((1054, 512))
        self.display = pygame.Surface((320, 240))
        self.clock = pygame.time.Clock()
        
        # estado del juego
        self.game_state = "MENU"  # menu playing
        
        # movimiento del jugador
        self.movement = [False, False]
        
        # cargar assets
        self.assets = {
            'caja': load_images('Tiles/caja', (16,16)),
            'piso': load_images('Tiles/pisos', (16,16)),
            'player': load_image('Reptiliano PJ/idle/pjbien.png', (12, 18)), 
            'buttons': load_images("botones"),
            'background': load_image("DJ Totote Fondo/DJ totote prime.png", (320, 240)),
            'player/idle' : Animation(load_images("Reptiliano PJ/idle"), img_dur=18),
            'player/run' : Animation(load_images("Reptiliano PJ/run"), img_dur=6),
            'player/jump' : Animation(load_images("Reptiliano PJ/jump"), img_dur=18, loop=False),
        }

        # cargar fondo del menú
        self.menu_bg = load_image("Obama_PJ/Menu_chad_sin_botones.png", (320, 240))
        
        # crear entidades del juego
        self.player = Player(self, (50, 50), (11, 16))
        self.tilemap = Tilemap(self, tile_size=16)
        
        # crear menú
        self.menu = Menu(self)
        self.scroll = [0, 30]


    def start_game(self):
        # inicia el juego
        self.game_state = "PLAYING"
    
    def back_to_menu(self):
        # volver al menú
        self.game_state = "MENU"
    
    def run(self):
        # arranque
        while True:
            # renderizar segun el estado
            if self.game_state == "MENU":
                self.menu.update()
                self.menu.render(self.display)
            elif self.game_state == "PLAYING":
                # render de lo que se muestra
                self.display.blit (self.assets['background'], (0,0))  # fondo 

                self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
                self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30
                render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

                self.tilemap.render(self.display, offset=self.scroll)
                self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
                self.player.render(self.display, offset = render_scroll)

            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit() # para salir
                
                # maneja eventos según el estado
                if self.game_state == "MENU":
                    self.menu.handle_events(event)
                elif self.game_state == "PLAYING":
                    # controles del juego
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                            self.movement[0] = True
                        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                            self.movement[1] = True
                        if event.key == pygame.K_UP or event.key == pygame.K_w:
                            self.player.velocity[1] = -3
                        if event.key == pygame.K_ESCAPE:
                            self.back_to_menu()  # volver al menú con ESC
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                            self.movement[0] = False
                        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                            self.movement[1] = False            
            
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0)) # escalar a pantalla
            pygame.display.update()
            self.clock.tick(60)

Game().run()