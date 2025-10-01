import sys
import pygame
from script.utils import load_image, load_images, Animation
from script.tilemap import Tilemap
from script.menu import Menu

RENDER_SCALE = 2.0

class Editor:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('editor')
        self.screen = pygame.display.set_mode((1054, 512))
        self.display = pygame.Surface((320, 240))
        self.clock = pygame.time.Clock()
        
        # cargar assets
        self.assets = {
            'caja': load_images('Tiles/caja', (16,16)),
            'piso': load_images('Tiles/pisos', (16,16)), 
        }

        self.movement = [False, False, False, False]

        self.tilemap = Tilemap(self, tile_size=16)
        
        self.scroll = [0, 0]
        
        self.tile_list = list(self.assets)
        self.tile_group = 0
        self.tile_variant = 0

        self.clicking = True
        self.right_clicking = False


    def run(self):
        # arranque
        while True:
            self.display.fill ((0, 0, 0))  # fondo 

            current_tile_img = self.assets[self.tile_list[self.tile_group]][self.tile_variant].copy()
            current_tile_img.set_alpha (100)

            self.display.blit(current_tile_img, (5, 5))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit() # para salir
                if event.type == pygame.MOUSEBUTTONDOWN :
                    if event.button == 1 :
                        self.clicking = True 
                    if event.button == 3 :
                        self.right_clicking = True
                    if event.button == 4 :
                        self.tile_group = (self.tile_group - 1) % len (self.tile_list)
                    if event.button == 5 :
                        self.tile_group = (self.tile_group + 1) % len (self.tile_list)
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.movement[1] = True
                    if event.key == pygame.K_UP or pygame.K_w :
                        self.movement [2] = True
                    if event.key == pygame.K_DOWN or pygame.K_s :
                        self.movement [3] = True

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.movement[1] = False
                    if event.key == pygame.K_UP or pygame.K_w:
                        self.movement [2] = False
                    if event.key == pygame.K_DOWN or pygame.K_s :
                        self.movement [3] = False            
        
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0)) # escalar a pantalla
            pygame.display.update()
            self.clock.tick(60)

Editor().run()