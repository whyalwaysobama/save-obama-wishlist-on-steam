import pygame
from script.utils import load_image

class Button:
    def __init__(self, x, y, normal_sprite, hover_sprite, action=None, scale=1.0):
        # escalar los sprites si se especifica
        if scale != 1.0:
            new_width = int(normal_sprite.get_width() * scale)
            new_height = int(normal_sprite.get_height() * scale)
            self.normal_sprite = pygame.transform.scale(normal_sprite, (new_width, new_height))
            self.hover_sprite = pygame.transform.scale(hover_sprite, (new_width, new_height))
        # sino usarlos normal
        else:
            self.normal_sprite = normal_sprite
            self.hover_sprite = hover_sprite
            
        self.x = x
        self.y = y # x y y para las posiciones
        self.action = action 
        self.is_hovered = False # mouse encima del sprite
        self.rect = pygame.Rect(x, y, self.normal_sprite.get_width(), self.normal_sprite.get_height()) # genera la hitbox
    
    def update(self, mouse_pos):
        # en caso de que este el mouse encima da true
        self.is_hovered = self.rect.collidepoint(mouse_pos)
    
    def render(self, surf):
        # si self.is_hovered es true usa el sprite cambiado
        sprite = self.hover_sprite if self.is_hovered else self.normal_sprite
        surf.blit(sprite, (self.x, self.y))
    
    def is_clicked(self, mouse_pos, mouse_clicked):
        # verifica si el boton se clickeo
        if self.rect.collidepoint(mouse_pos) and mouse_clicked:
            if self.action:
                self.action()
            return True
        return False

class Menu:
    def __init__(self, game):
        self.game = game
        self.current_menu = "MAIN"  # "MAIN", "CREDITS", "TUTORIAL"
        
        # crear botones
        self.create_buttons()
        
        # cargar fondos adicionales si existen
        self.credits_bg = load_image("fondo/fondo_sin_obama.png", (320, 240))
        
        self.tutorial_bg = load_image("fondo/fondo_sin_obama.png", (320, 240))
        
    
    def create_buttons(self):
        # carga los assets de los botones
        button_sprites = self.game.assets['buttons']
        
        # escala para achicar los botones
        scale = 0.5  
        
        # boton jugar - izquierda
        self.creditos_button = Button(
            x=200,
            y=150, # posicion 
            normal_sprite=button_sprites[0], 
            hover_sprite=button_sprites[1], # defino cada sprite
            action=self.show_credits, # cambio modo actual
            scale=scale # escala
        )
        
        # boton tutorial - arriba derecha
        self.tutorial_button = Button(
            x=200,
            y=105,
            normal_sprite=button_sprites[4],
            hover_sprite=button_sprites[5],
            action=self.show_tutorial,
            scale=scale 
        )
        # igual que el otro boton
        # boton creditos - abajo derecha
        self.jugar_button = Button(
            x=3,
            y=115,
            normal_sprite=button_sprites[2],
            hover_sprite=button_sprites[3],
            action=self.start_game,
            scale=0.4
        )
        
        # boton volver - para créditos y tutorial
        self.volver_button = Button(
            x=1,
            y=199,
            normal_sprite=button_sprites[6],
            hover_sprite=button_sprites[7],
            action=self.back_to_main,
            scale=0.45
        )
        # igual q arriba
        # listas de botones por menú
        self.main_buttons = [self.jugar_button, self.tutorial_button, self.creditos_button]
        self.credits_buttons = [self.volver_button]
        self.tutorial_buttons = [self.volver_button]
    
    def start_game(self):
        # iniciar el juego
        self.game.start_game()
    
    def show_credits(self):
        # mostrar pantalla de créditos
        self.current_menu = "CREDITS"
    
    def show_tutorial(self):
        # mostar pantalla de tutorial
        self.current_menu = "TUTORIAL"
    
    def back_to_main(self):
        # volver al menu principal
        self.current_menu = "MAIN"
    
    def get_scaled_mouse_pos(self):
        # obtener la posición del mouse escalada 
        mouse_pos = pygame.mouse.get_pos()
        return (mouse_pos[0] * 320 // 1054, mouse_pos[1] * 240 // 512)
    
    def update(self):
        # actualizar botones según el menú actual
        scaled_mouse_pos = self.get_scaled_mouse_pos()
        # cambia el sprite si esta el mouse encima
        if self.current_menu == "MAIN":
            for button in self.main_buttons:
                button.update(scaled_mouse_pos)
        elif self.current_menu == "CREDITS":
            for button in self.credits_buttons:
                button.update(scaled_mouse_pos)
        elif self.current_menu == "TUTORIAL":
            for button in self.tutorial_buttons:
                button.update(scaled_mouse_pos)
    
    def handle_events(self, event):
        # manejar eventos del menu
        scaled_mouse_pos = self.get_scaled_mouse_pos()
        mouse_clicked = event.type == pygame.MOUSEBUTTONDOWN and event.button == 1

        if self.current_menu == "MAIN":
            for button in self.main_buttons:
                button.is_clicked(scaled_mouse_pos, mouse_clicked)
        elif self.current_menu == "CREDITS":
            for button in self.credits_buttons:
                button.is_clicked(scaled_mouse_pos, mouse_clicked)
        elif self.current_menu == "TUTORIAL":
            for button in self.tutorial_buttons:
                button.is_clicked(scaled_mouse_pos, mouse_clicked)
    
    def render_credits_text(self, surf):
        # renderizar texto de creditos
        font = pygame.font.Font(None, 24)
        title_font = pygame.font.Font(None, 32)
        
        
        # informacion de créditos
        credits_lines = [
            "Creadores:",
            "Santiago Chaparro",
            "Dante Zurlo", 
            "Juan Giuri",
            "",
            "Why Always Obama?",
            "",
            "Gracias por jugar!"
        ]
        
        y = 60
        for line in credits_lines:
            if line:
                text_surface = font.render(line, True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=(160, y))
                surf.blit(text_surface, text_rect)
            y += 18
    
    def render_tutorial_text(self, surf):
        # renderizar texto de tutorial (controles)
        font = pygame.font.Font(None, 20)
        title_font = pygame.font.Font(None, 28)
        
        
        # instrucciones
        tutorial_lines = [
            "Controles:",
            "",
            "Flechas o WASD para moverse",
            "",
            "Flecha arriba / W: Saltar",
            "Flecha izq / A: Mover izquierda",
            "Flecha der / D: Mover derecha", 
            "",
            "ESC: Volver al menu",
        ]
        
        y = 60
        for line in tutorial_lines:
            if line:
                text_surface = font.render(line, True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=(160, y))
                surf.blit(text_surface, text_rect)
            y += 16
    
    def render(self, surf):
        # renderizar el menu segun el estado actual
        if self.current_menu == "MAIN":
            # renderizar fondo del menú principal
            surf.blit(self.game.menu_bg, (0, 0))
            
            # renderizar botones principales
            for button in self.main_buttons:
                button.render(surf)
                
        elif self.current_menu == "CREDITS":
            # renderizar fondo de créditos
            surf.blit(self.credits_bg, (0, 0))
            
            # renderizar texto de créditos
            self.render_credits_text(surf)
            
            # renderizar botón de volver
            for button in self.credits_buttons:
                button.render(surf)

            for event in pygame.event.get() :
                if event.type == pygame.KEYDOWN :
                    if event.key == pygame.K_ESCAPE:
                        self.back_to_main()  
                
        elif self.current_menu == "TUTORIAL":
            # renderizar fondo de tutorial
            surf.blit(self.tutorial_bg, (0, 0))
            
            # renderizar texto de tutorial
            self.render_tutorial_text(surf)
            
            # renderizar botón de volver
            for button in self.tutorial_buttons:
                button.render(surf)
            
            for event in pygame.event.get() :
                if event.type == pygame.KEYDOWN :
                    if event.key == pygame.K_ESCAPE:
                        self.back_to_main()  