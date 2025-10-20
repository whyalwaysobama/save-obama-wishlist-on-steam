import sys
import pygame
from script.utils import load_image, load_images, Animation
from script.entitites import PhysicsEntity, Player
from script.tilemap import Tilemap
from script.menu import Menu
from script.save_progress import SaveProgress

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
        self.max_time = 15
        self.collected_stars = set()
        self.current_level = 1
        self.fps = 60
        self.level_configs = {
            'tutorial': {'max_time': None, 'start_pos': [30, 100]},
            1: {'max_time': 40, 'start_pos': [0, 115]},
            2: {'max_time': 18, 'start_pos': [0, 115]},
            3: {'max_time': 35, 'start_pos': [0, 115]},
        }
        self.level_maps = {
            'tutorial': 'tuto.json',
            1: '1.json',
            2: '2.json',
            3: '3.json',
            4: '4.json',
            5: '5.json',
            6: '6.json',
            7: '7.json',
            8: '8.json',
            9: '9.json',
            10: '10.json',
            11: 'secreto.json',
        }
        self.slowmo = False
        
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
            'elmatador' : load_images('Tiles/elmatador'),
            'background': load_image("DJ Totote Fondo/DJ totote prime.png", (320, 240)),
            'player/idle' : Animation(load_images("Reptiliano PJ/idle"), img_dur=18),
            'player/run' : Animation(load_images("Reptiliano PJ/run"), img_dur=6),
            'player/jump' : Animation(load_images("Reptiliano PJ/jump"), img_dur=10, loop=False),
            'player/save' : Animation(load_images("Reptiliano PJ/salvador"), img_dur=18, loop=False),
            'level 1' : load_images("Niveles/Nivel 1", (130, 230)),
            'level 2' : load_images("Niveles/Nivel 2", (130, 230)),
            'level 3' : load_images("Niveles/Nivel 3", (130, 230)),
            'level 4' : load_images("Niveles/Nivel 4", (130, 230)),
            'level 5' : load_images("Niveles/Nivel 5", (130, 230)),
            'level 6' : load_images("Niveles/Nivel 6", (130, 230)),
            'level 7' : load_images("Niveles/Nivel 7", (130, 230)),
            'level 8' : load_images("Niveles/Nivel 8", (130, 230)),
            'level 9' : load_images("Niveles/Nivel 9", (130, 230)),
            'level 10' : load_images("Niveles/Nivel 10", (130, 230)),
        }
        
        # cargar fondo del menú
        self.menu_bg = load_image("Obama_PJ/Menu_chad_sin_botones.png", (320, 240))
        
        # crear entidades del juego
        self.player = Player(self, (50, 50), (11, 16))
        self.tilemap = Tilemap(self, tile_size=16)
        self.tilemap.load('3.json')

        # crear menú
        self.menu = Menu(self)
        self.scroll = [0, 30]

        self.save_progress = SaveProgress()

    def load_level(self, level_id):
        if level_id in self.level_maps:
            self.current_level = level_id
            map_file = self.level_maps[level_id]
            
            # Reiniciar tilemap
            self.tilemap = Tilemap(self, tile_size=16)
            self.tilemap.load(map_file)
            
            # Reiniciar estrellas colectadas para este nivel
            self.collected_stars = set()
            
            config = self.level_configs.get(level_id, {'max_time': 15, 'start_pos': [0, 0]})
            self.max_time = config['max_time'] 
            self.player.pos = config['start_pos'][:]

            return True
        else:
            return False

    def start_game(self, level_id=1):
        # inicia el juego
        if not self.load_level(level_id):
            return
        saved_stars = self.save_progress.get_level_stars(level_id)
        self.game_state = "PLAYING"  # posición inicial
        self.player.velocity = [0, 0]  # velocidad en 0
        self.player.air_time = 0      
        self.player.dashing = False  
        self.player.animation_locked = False
        self.player.dash_time = 0
        self.player.dash_cooldown = 30  
        self.player.set_action("idle")  
        self.movement = [False, False]  
        self.timer = 0
        self.timer_running = True
        self.scroll = [0, 30]
        self.clicking = False
        self.fps = 60
        self.slowmo = False
        
    
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
                if self.max_time is not None and self.timer >= self.max_time :
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
                        if event.key == pygame.K_LSHIFT:
                            self.slowmo = True
                            self.fps = 30
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                            self.movement[0] = False
                        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                            self.movement[1] = False
                        if event.key == pygame.K_e:
                            self.clicking = False 
                        if event.key == pygame.K_LSHIFT:
                            self.slowmo = False
                            self.fps = 60
                elif self.game_state == "WIN":
                    self.display.blit(load_image("fondo/win.png", (320, 240)), (0, 0))
                    self.timer_running = False
                    stars_in_level = len(self.collected_stars)
                    self.save_progress.update_level(
                        self.current_level,
                        stars_in_level,
                        self.timer,
                        completed=True
                    )
                    self.timer = 0

                    if event.type == pygame.KEYDOWN :
                        if event.key == pygame.K_ESCAPE:
                            self.back_to_menu()  
                elif self.game_state == "LOSE":
                    self.menu.handle_events(event)                

            
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0)) # escalar a pantalla
            pygame.display.update()
            self.clock.tick(self.fps)

Game().run()