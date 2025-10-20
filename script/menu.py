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
        self.current_menu = "MAIN"  # "MAIN", "CREDITS", "TUTORIAL", "LEVELS", "LOSE"
        
        # estado del modal de niveles
        self.modal_open = False
        self.selected_level = None
        
        # overlay oscuro para el modal
        self.overlay = pygame.Surface((320, 240))
        self.overlay.set_alpha(180)  # transparencia
        self.overlay.fill((0, 0, 0))  # negro
        
        # definir zonas clickeables de niveles (x, y, ancho, alto)
        self.level_zones = [
            {"rect": pygame.Rect(7, 22, 19, 38), "id": 1, "name": "Nivel 1"},
            {"rect": pygame.Rect(56, 10, 19, 38), "id": 2, "name": "Nivel 2"},
            {"rect": pygame.Rect(75, 52, 19, 38), "id": 3, "name": "Nivel 3"},
            {"rect": pygame.Rect(226, 25, 29, 35), "id": 4, "name": "Nivel 4"},
            {"rect": pygame.Rect(255, 38, 80, 38), "id": 5, "name": "Nivel 5"},
            {"rect": pygame.Rect(227, 85, 29, 30), "id": 6, "name": "Nivel 6"},
            {"rect": pygame.Rect(256, 100, 24, 34), "id": 7, "name": "Nivel 7"},
            {"rect": pygame.Rect(280, 121, 20, 30), "id": 8, "name": "Nivel 8"},
            {"rect": pygame.Rect(22, 102, 63, 55), "id": 9, "name": "Nivel 9"},
            {"rect": pygame.Rect(155, 150, 115, 37), "id": 10, "name": "Nivel 10"},
            {"rect": pygame.Rect(157, 68, 45, 80), "id": 11, "name": "Nivel Secreto"},
        ]
        
        self.easter_egg = pygame.Rect(2, 128, 17, 28)
        self.eater_shown = False
            

        # crear botones
        self.create_buttons()
        
        # cargar fondos adicionales si existen
        self.credits_bg = load_image("fondo/fondo_sin_obama.png", (320, 240))
        self.tutorial_bg = load_image("fondo/fondo_sin_obama.png", (320, 240))
        self.levels_bg = load_image("Niveles/Niveles sin sida.png", (320, 240))
        self.death_bg = load_image("fondo/fondo_sin_obama.png", (320, 240))
        
    def start_tutorial_level(self):
            self.game.start_game('tutorial')  # Asumiendo que el tutorial es el nivel 0

    def start_selected_level(self):
        if self.selected_level:
            level_id = self.selected_level['id']
            print(f"Iniciando {self.selected_level['name']} (ID: {level_id})")
            # aquí después pasarás el ID del nivel a start_game
            self.game.start_game(level_id)
            self.close_modal()

    def retry_level(self):
        # reinicia el nivel actual (fallback a 'tutorial' si no hay current_level)
        level_id = getattr(self.game, 'current_level', None)
        if level_id is None:
            level_id = 'tutorial'
        self.game.start_game(level_id)
        # limpiar estado del menú por si quedó abierto
        self.modal_open = False
        self.selected_level = None
        self.current_menu = "MAIN"

    
    def create_buttons(self):
        # carga los assets de los botones
        button_sprites = self.game.assets['buttons']
        play_sprites = self.game.assets['p_button']
        
        # escala para achicar los botones
        scale = 0.5  
        
        self.continue_button = Button(
            x=215,
            y=196, # posicion 
            normal_sprite=button_sprites[1], 
            hover_sprite=button_sprites[0], # defino cada sprite
            action=self.start_tutorial_level, # cambio modo actual
            scale=scale # escala
        ) 

        # boton creditos - izquierda
        self.creditos_button = Button(
            x=200,
            y=150, # posicion 
            normal_sprite=button_sprites[2], 
            hover_sprite=button_sprites[3], # defino cada sprite
            action=self.show_credits, # cambio modo actual
            scale=scale # escala
        )
        
        # boton tutorial - arriba derecha
        self.tutorial_button = Button(
            x=200,
            y=105,
            normal_sprite=button_sprites[8],
            hover_sprite=button_sprites[9],
            action=self.show_tutorial,
            scale=scale
        )
        
        # boton jugar - abajo izquierda (VA A NIVELES)
        self.jugar_button = Button(
            x=3,
            y=115,
            normal_sprite=button_sprites[4],
            hover_sprite=button_sprites[5],
            action=self.show_levels,  
            scale=0.4
        )
        
        # boton volver - para créditos, tutorial y niveles
        self.volver_button = Button(
            x=1,
            y=199,
            normal_sprite=button_sprites[10],
            hover_sprite=button_sprites[11],
            action=self.back_to_main,
            scale=0.45
        )
        
        # boton play para el modal de niveles
        self.play_modal_button = Button(
            x=125,
            y=140,
            normal_sprite=play_sprites[1],
            hover_sprite=play_sprites[0],
            action=self.start_selected_level,
            scale=0.6
        )
        
        # boton cerrar modal
        self.close_modal_button = Button(
            x=240,
            y=200,
            normal_sprite=button_sprites[10],
            hover_sprite=button_sprites[11],
            action=self.close_modal,
            scale=0.35
        )
        self.retry_button = Button(
            x=215,
            y=196, # posicion 
            normal_sprite=button_sprites[7], 
            hover_sprite=button_sprites[6], # defino cada sprite
            action=self.retry_level, # cambio modo actual
            scale=scale # escala
        )
        
        # listas de botones por menú
        self.main_buttons = [self.jugar_button, self.tutorial_button, self.creditos_button]
        self.credits_buttons = [self.volver_button]
        self.tutorial_buttons = [self.volver_button, self.continue_button]
        self.levels_buttons = [self.volver_button]  # por ahora solo volver
        self.death_buttons = [self.volver_button, self.retry_button]
    
    def show_levels(self):
        # mostrar selector de niveles
        self.current_menu = "LEVELS"
    
    def open_modal(self, level_zone):
        # abrir modal con info del nivel
        self.modal_open = True
        self.selected_level = level_zone
    
    def close_modal(self):
        # cerrar modal
        self.modal_open = False
        self.selected_level = None

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
        self.game.game_state = "MENU"
    
    def show_death (self):
        # mostrar pantalla de muerte
        self.current_menu = "LOSE"
    
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
        elif self.current_menu == "LEVELS":
            if self.modal_open:
                # actualizar botones del modal
                self.play_modal_button.update(scaled_mouse_pos)
                self.close_modal_button.update(scaled_mouse_pos)
            else:
                # actualizar botón volver
                for button in self.levels_buttons:
                    button.update(scaled_mouse_pos)
        elif self.current_menu == "LOSE":
            for button in self.death_buttons:
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
            # use the passed event to detect ESC (don't poll events here)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.back_to_main()
        elif self.current_menu == "TUTORIAL":
            for button in self.tutorial_buttons:
                button.is_clicked(scaled_mouse_pos, mouse_clicked)
            # use the passed event to detect ESC (don't poll events here)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.back_to_main()
        elif self.current_menu == "LEVELS":
            if self.modal_open:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.close_modal()  # cerrar el modal y volver al menú de niveles
                # manejar clicks en el modal
                if mouse_clicked:
                    self.play_modal_button.is_clicked(scaled_mouse_pos, mouse_clicked)
                    self.close_modal_button.is_clicked(scaled_mouse_pos, mouse_clicked)
            else:
                # verificar clicks en zonas de niveles
                if mouse_clicked:
                    for zone in self.level_zones:
                        try:
                            if zone["rect"].collidepoint(scaled_mouse_pos):
                                self.open_modal(zone)
                                
                        except:
                            pass
                    # si no clickeó en ningún nivel, verificar botón volver
                    for button in self.levels_buttons:
                        button.is_clicked(scaled_mouse_pos, mouse_clicked)
        elif self.current_menu == "LOSE":
            for button in self.death_buttons:
                button.is_clicked(scaled_mouse_pos, mouse_clicked)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.back_to_main()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.retry_level()
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
    
    def render_death_text(self, surf):
        # renderizar texto de creditos
        font = pygame.font.Font(None, 24)
        title_font = pygame.font.Font(None, 32)
        
        
        # informacion de créditos
        credits_lines = [
            "Fallaste",
            "",
            "Obama no pudo ser salvado.",
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
            "E: Tirarse",
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
                
        elif self.current_menu == "TUTORIAL":
            # renderizar fondo de tutorial
            surf.blit(self.tutorial_bg, (0, 0))
            
            # renderizar texto de tutorial
            self.render_tutorial_text(surf)
            
            # renderizar botón de volver
            for button in self.tutorial_buttons:
                button.render(surf)
        
        elif self.current_menu == "LEVELS":
            # renderizar selector de niveles
            surf.blit(self.levels_bg, (0, 0))

            #for zone in self.level_zones:
                #pygame.draw.rect(surf, (255, 0, 0), zone["rect"], 2)
            
            # si el modal está abierto, renderizarlo
            if self.modal_open:
                self.render_modal(surf)
            else:
                # renderizar botón de volver
                for button in self.levels_buttons:
                    button.render(surf)
        elif self.current_menu == "LOSE":
            surf.blit(load_image("fondo/lose.png", (320, 240)), (0, 0))
            for button in self.death_buttons:
                button.render(surf)
            
    def render_modal(self, surf):
        # dibujar overlay oscuro
        surf.blit(self.overlay, (0, 0))
        
        # renderizar imagen del nivel según el id
        level_id = self.selected_level['id']
        asset_key = f'level {level_id}'
        if asset_key in self.game.assets:
            level_img = self.game.assets[asset_key][0]  # usa la primera imagen si es una lista
            img_rect = level_img.get_rect(center=(160, 120))
            surf.blit(level_img, img_rect)
        
        # renderizar texto del nivel
        font_title = pygame.font.Font(None, 28)
        title_text = font_title.render(self.selected_level['name'], True, (0, 0, 0))
        title_rect = title_text.get_rect(center=(160, 25))
        surf.blit(title_text, title_rect)
        
        # renderizar botones del modal
        self.play_modal_button.render(surf)
        self.close_modal_button.render(surf)