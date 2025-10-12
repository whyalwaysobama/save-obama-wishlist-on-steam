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
        self.clicking = False
        self.timer = 0
        self.timer_running = False
        self.max_time = 5
        self.collected_stars = set()
        
        # estado del juego
        self.game_state = "MENU"  # menu playing
        
        # movimiento del jugador
        self.movement = [False, False]
        
        # cargar assets
        self.assets = {
            'caja': load_images('Tiles/caja', (16,16)),
            'piso': load_images('Tiles/pisos', (16,16)),
            'silla': load_images('Tiles/silla'),
            'player': load_image('Reptiliano PJ/idle/pjbien.png', (12, 18)), 
            'buttons': load_images("botones"),
            'p_button': load_images("Niveles/botones_jugar"),
            'barrier' : load_images('Tiles/barrier'),
            'obama' : load_images("Obama_PJ"),
            'laser' : load_images('Tiles/laser'),
            'barril' : load_images('Tiles/barbarril'),
            'estrella' : load_images('Tiles/estrella'),
            'people' : load_images('Tiles/personas'),
            'pisos variables' : load_images('Tiles/pisos variables'),
            'background': load_image("DJ Totote Fondo/DJ totote prime.png", (320, 240)),
            'player/idle' : Animation(load_images("Reptiliano PJ/idle"), img_dur=18),
            'player/run' : Animation(load_images("Reptiliano PJ/run"), img_dur=6),
            'player/jump' : Animation(load_images("Reptiliano PJ/jump"), img_dur=10, loop=False),
            'player/save' : Animation(load_images("Reptiliano PJ/salvador"), img_dur=18, loop=False),
        }
        
        # cargar fondo del menú
        self.menu_bg = load_image("Obama_PJ/Menu_chad_sin_botones.png", (320, 240))
        
        # crear entidades del juego
        self.player = Player(self, (50, 50), (11, 16))
        self.tilemap = Tilemap(self, tile_size=16)
        self.tilemap.load('tuto.json')

        # crear menú
        self.menu = Menu(self)
        self.scroll = [0, 30]


    def start_game(self):
        # inicia el juego
        self.game_state = "PLAYING"
        self.player.pos = [0, 0]  # posición inicial
        self.player.velocity = [0, 0]  # velocidad en 0
        self.player.air_time = 0      
        self.player.dashing = False  
        self.player.animation_locked = False
        self.player.dash_time = 0
        self.player.dash_cooldown = 0  
        self.player.set_action("idle")  
        self.movement = [False, False]  
        self.timer = 0
        self.timer_running = True
    
    def back_to_menu(self):
        # volver al menú
        self.game_state = "MENU"
        self.menu.current_menu = "MAIN"
    
    def run(self):
        # arranque
        while True:
            # renderizar segun el estado
            if self.game_state == "MENU":
                self.timer = 0
                self.menu.update()
                self.menu.render(self.display)
            elif self.game_state == "PLAYING":
                # render de lo que se muestra
                self.display.blit (self.assets['background'], (0,0))  # fondo 

                self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
                self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30
                render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

                self.tilemap.render(self.display, offset=self.scroll)
                self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0), clicking=self.clicking)
                self.player.render(self.display, offset = render_scroll)

                star_collected = self.tilemap.check_star_collision(self.player.rect())
                if star_collected:
                    self.collected_stars.add(star_collected)

                if self.tilemap.check_obama_collision (self.player.rect()) :
                    self.game_state = "WIN"
            
            elif self.game_state == "LOSE":
                    self.menu.show_death()
                    self.menu.update()
                    self.menu.render(self.display)
            
            if self.timer_running :
                self.timer += 1/60
                if self.timer >= self.max_time :
                    self.timer = self.max_time
                    self.timer_running = False
                    self.game_state = "LOSE"  
            
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
                        if (event.key == pygame.K_UP or event.key == pygame.K_w or event.key == pygame.K_SPACE) and not self.player.dashing and self.player.air_time < 6 :
                            self.player.velocity[1] = -3
                        if event.key == pygame.K_e: 
                            self.clicking = True
                        if event.key == pygame.K_ESCAPE:
                            self.back_to_menu()  # volver al menú con ESC
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                            self.movement[0] = False
                        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                            self.movement[1] = False
                        if event.key == pygame.K_e:
                            self.clicking = False 
                elif self.game_state == "WIN":
                    self.display.blit(load_image("fondo/win.png", (320, 240)), (0, 0))
                    if event.type == pygame.KEYDOWN :
                        if event.key == pygame.K_ESCAPE:
                            self.back_to_menu()  
                elif self.game_state == "LOSE":
                    self.menu.handle_events(event)                

            
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0)) # escalar a pantalla
            pygame.display.update()
            self.clock.tick(60)

Game().run()