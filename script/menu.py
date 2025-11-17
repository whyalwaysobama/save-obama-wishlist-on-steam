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
    
    def render(self, surf, disabled=False):
        # si está deshabilitado, mostrar en gris
        if disabled:
            # Crear una versión gris del sprite
            gray_sprite = self.normal_sprite.copy()
            gray_sprite.fill((100, 100, 100), special_flags=pygame.BLEND_RGB_MULT)
            surf.blit(gray_sprite, (self.x, self.y))
        # sino, mostrar normal o hover
        else:
            sprite = self.hover_sprite if self.is_hovered else self.normal_sprite
            surf.blit(sprite, (self.x, self.y))
    
    def is_clicked(self, mouse_pos, mouse_clicked, disabled=False):
        # verifica si el boton se clickeo
        if self.rect.collidepoint(mouse_pos) and mouse_clicked and not disabled:
            if self.action:
                self.action()
            return True
        return False

class Menu:
    def __init__(self, game):
        self.game = game
        self.current_menu = "MAIN"  # "MAIN", "CREDITS", "TUTORIAL", "LEVELS", "LOSE", "SAVES"
        
        # estado del modal de niveles
        self.modal_open = False
        self.selected_level = None
        
        # overlay oscuro para el modal
        self.overlay = pygame.Surface((320, 240))
        self.overlay.set_alpha(180)  # transparencia
        self.overlay.fill((0, 0, 0))  # negro
        
        # overlay gris para niveles bloqueados
        self.gray_overlay = pygame.Surface((320, 240))
        self.gray_overlay.set_alpha(180)  # transparencia
        self.gray_overlay.fill((100, 100, 100))  # gris
        
        # definir zonas clickeables de niveles (x, y, ancho, alto)
        self.level_zones = [
            {"rect": pygame.Rect(7, 22, 19, 38), "id": 1, "name": "Nivel 1"},
            {"rect": pygame.Rect(56, 10, 19, 37), "id": 2, "name": "Nivel 2"},
            {"rect": pygame.Rect(75, 52, 19, 38), "id": 3, "name": "Nivel 3"},
            {"rect": pygame.Rect(255, 38, 80, 38), "id": 6, "name": "Nivel 6"},
            {"rect": pygame.Rect(226, 25, 29, 35), "id": 5, "name": "Nivel 5"},
            {"rect": pygame.Rect(256, 100, 24, 34), "id": 8, "name": "Nivel 8"},
            {"rect": pygame.Rect(227, 85, 29, 30), "id": 7, "name": "Nivel 7"},
            {"rect": pygame.Rect(22, 102, 63, 55), "id": 4, "name": "Nivel 4"},
            {"rect": pygame.Rect(280, 121, 20, 30), "id": 9, "name": "Nivel 9"},
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
        self.saves_bg = load_image("fondo/fondo_sin_obama.png", (320, 240))
        
    def start_tutorial_level(self):
            self.game.start_game('tutorial') 

    def start_selected_level(self):
        if self.selected_level:
            level_id = self.selected_level['id']
            # Verificar si el nivel está desbloqueado antes de iniciar
            if self.game.save_progress.is_level_unlocked(level_id):
                print(f"Iniciando {self.selected_level['name']} (ID: {level_id})")
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
        
        self.delete1_button = Button(
            x=208,
            y=30, # posicion 
            normal_sprite=button_sprites[1], 
            hover_sprite=button_sprites[0], # defino cada sprite
            action=lambda i=0: self.delete_save(i), # cambio modo actual
            scale=0.25 # escala
        )
        
        self.delete2_button = Button(
            x=208,
            y=90, # posicion 
            normal_sprite=button_sprites[1], 
            hover_sprite=button_sprites[0], # defino cada sprite
            action=lambda i=1: self.delete_save(i), # cambio modo actual
            scale=0.25 # escala
        )

        self.delete3_button = Button(
            x=208,
            y=150, # posicion 
            normal_sprite=button_sprites[1], 
            hover_sprite=button_sprites[0], # defino cada sprite
            action=lambda i=2: self.delete_save(i), # cambio modo actual
            scale=0.25 # escala
        )

        self.continue_after_w_button = Button(
            x=215,
            y=196, # posicion 
            normal_sprite=button_sprites[9], 
            hover_sprite=button_sprites[8], # defino cada sprite
            action=self.show_levels, # cambio modo actual
            scale=scale # escala
        )

        self.retry_after_w_button = Button(
            x=1,
            y=196, # posicion 
            normal_sprite=button_sprites[15], 
            hover_sprite=button_sprites[14], # defino cada sprite
            action=self.retry_level, # cambio modo actual
            scale=scale # escala
        )

        self.continue_button = Button(
            x=215,
            y=196, # posicion 
            normal_sprite=button_sprites[9], 
            hover_sprite=button_sprites[8], # defino cada sprite
            action=self.start_tutorial_level, # cambio modo actual
            scale=scale # escala
        ) 

        # boton creditos - izquierda
        self.creditos_button = Button(
            x=200,
            y=150, # posicion 
            normal_sprite=button_sprites[10], 
            hover_sprite=button_sprites[11], # defino cada sprite
            action=self.show_credits, # cambio modo actual
            scale=scale # escala
        )
        
        # boton tutorial - arriba derecha
        self.tutorial_button = Button(
            x=200,
            y=105,
            normal_sprite=button_sprites[16],
            hover_sprite=button_sprites[17],
            action=self.show_tutorial,
            scale=scale
        )
        
        # boton jugar - abajo izquierda (VA A NIVELES)
        self.jugar_button = Button(
            x=3,
            y=115,
            normal_sprite=button_sprites[12],
            hover_sprite=button_sprites[13],
            action=self.show_saves,  
            scale=0.4
        )
        
        # boton volver - para créditos, tutorial y niveles
        self.volver_button = Button(
            x=1,
            y=196,
            normal_sprite=button_sprites[18],
            hover_sprite=button_sprites[19],
            action=self.back_to_main,
            scale=scale
        )
        
        self.volver_saves_button = Button(
            x=1,
            y=199,
            normal_sprite=button_sprites[18],
            hover_sprite=button_sprites[19],
            action=self.show_saves,
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
            normal_sprite=button_sprites[18],
            hover_sprite=button_sprites[19],
            action=self.close_modal,
            scale=0.35
        )
        self.retry_button = Button(
            x=215,
            y=196, # posicion 
            normal_sprite=button_sprites[15], 
            hover_sprite=button_sprites[14], # defino cada sprite
            action=self.retry_level, # cambio modo actual
            scale=scale # escala
        )
        
        self.save1_button = Button(
            x=103,
            y=30, # posicion 
            normal_sprite=button_sprites[3], 
            hover_sprite=button_sprites[2], # defino cada sprite
            action=lambda i=0: self.on_save_clicked(i), # cambio modo actual
            scale=0.25 # escala
        )

        self.save2_button = Button(
            x=103,
            y=90, # posicion 
            normal_sprite=button_sprites[5], 
            hover_sprite=button_sprites[4], # defino cada sprite
            action=lambda i=1: self.on_save_clicked(i), # cambio modo actual
            scale=0.25 # escala
        )

        self.save3_button = Button(
            x=103,
            y=150, # posicion 
            normal_sprite=button_sprites[7], 
            hover_sprite=button_sprites[6], # defino cada sprite
            action=lambda i=2: self.on_save_clicked(i), # cambio modo actual
            scale=0.25 # escala
        )

        # listas de botones por menú
        self.main_buttons = [self.jugar_button, self.tutorial_button, self.creditos_button]
        self.credits_buttons = [self.volver_button]
        self.tutorial_buttons = [self.volver_button, self.continue_button]
        self.win_buttons = [self.continue_after_w_button, self.retry_after_w_button]
        self.levels_buttons = [self.volver_saves_button] 
        self.death_buttons = [self.volver_button, self.retry_button]
        self.saves_buttons = [self.save1_button, self.save2_button, self.save3_button, self.volver_button, self.delete1_button, self.delete2_button, self.delete3_button]
    
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

    def show_saves (self) :
        self.current_menu = "SAVES"
        self.update_saves_info()
    
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
    
    def delete_save (self, slot) :
        sp = self.game.save_progress
        if not sp :
            return False
        
        if sp.current_slot == slot :
            sp.current_slot = None
            sp.data = None
        
        try:
            success = sp.delete_save(slot)
        except Exception :
            success = False

        self.update_saves_info()
        return success

    def update_saves_info(self) :
        self.saves_info = [None, None, None]
        sp = self.game.save_progress
        
        if sp:
            saves_list = sp.list_saves()
            for i, save_data in enumerate(saves_list):
                self.saves_info[i] = save_data

    def on_save_clicked(self, slot_index):
        sp = self.game.save_progress
        if sp.save_exists (slot_index) :
            sp.load(slot_index)
        else: 
            sp.create (slot_index)

        self.show_levels()
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
        elif self.current_menu == "SAVES":
            for button in self.saves_buttons:
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
        elif self.current_menu == "WIN" :
            for button in self.win_buttons :
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
                    # Verificar si el nivel está desbloqueado para habilitar/deshabilitar el botón
                    level_id = self.selected_level['id']
                    is_unlocked = self.game.save_progress.is_level_unlocked(level_id)
                    self.play_modal_button.is_clicked(scaled_mouse_pos, mouse_clicked, disabled=not is_unlocked)
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
        elif self.current_menu == "WIN" :
            for button in self.win_buttons :
                button.is_clicked(scaled_mouse_pos, mouse_clicked)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.back_to_main()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.retry_level()
        elif self.current_menu == "SAVES" :
            for button in self.saves_buttons :
                button.is_clicked(scaled_mouse_pos, mouse_clicked)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE :
                self.back_to_main ()

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
        font = pygame.font.Font(None, 18)
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
            "R: Reiniciar nivel",
            "Left Shift: Slow motion",
            "ESC: Volver al menu",
        ]
        
        y = 25
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
            surf.blit(self.game.huergo, (240, 10))
            
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
            
            # si el modal está abierto, renderizarlo
            if self.modal_open:
                self.render_modal(surf)
            else:
                # renderizar botón de volver
                for zone in self.level_zones:
                    rect = zone["rect"]

                    overlay = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
                    unlocked = False 

                    try :
                        unlocked = bool(self.game.save_progress.is_level_unlocked(zone["id"]))
                    except Exception:
                        pass
                    
                    if unlocked:
                        # dorado semi-transparente
                        overlay.fill((212, 175, 55, 145))  # RGBA dorado
                    else:
                        # grisáceo semi-transparente
                        overlay.fill((190, 190, 200, 145))  # RGBA grisáceo

                    surf.blit(overlay, rect.topleft)

                for button in self.levels_buttons:
                    button.render(surf)

        elif self.current_menu == "LOSE":
            surf.blit(load_image("fondo/lose.png", (320, 240)), (0, 0))
            for button in self.death_buttons:
                button.render(surf)
        elif self.current_menu == "WIN" :
            surf.blit(load_image("fondo/win.png", (320, 240)), (0,0))
            for button in self.win_buttons :
                button.render(surf)
        elif self.current_menu == "SAVES" :
            surf.blit(self.saves_bg, (0,0))
            for button in self.saves_buttons :
                button.render(surf)
            
    def render_modal(self, surf):
        # dibujar overlay oscuro
        surf.blit(self.overlay, (0, 0))
        
        # Verificar si el nivel está desbloqueado
        level_id = self.selected_level['id']
        is_unlocked = self.game.save_progress.is_level_unlocked(level_id)
        
        # renderizar imagen del nivel según el id
        asset_key = f'level {level_id}'
        if asset_key in self.game.assets:
            stars = self.game.save_progress.get_level_stars(level_id)
            img_index = min(stars, 3)  
            level_img = self.game.assets[asset_key][img_index]
            img_rect = level_img.get_rect(center=(160, 120))
            surf.blit(level_img, img_rect)
            
            # Si el nivel no está desbloqueado, aplicar overlay gris
            if not is_unlocked:
                gray_surface = pygame.Surface((level_img.get_width(), level_img.get_height()))
                gray_surface.set_alpha(180)  # Transparencia
                gray_surface.fill((100, 100, 100))  # Color gris
                surf.blit(gray_surface, img_rect)
        
        # renderizar texto del nivel
        font_title = pygame.font.Font(None, 28)
        title_text = font_title.render(self.selected_level['name'], True, (0, 0, 0))
        title_rect = title_text.get_rect(center=(160, 25))
        surf.blit(title_text, title_rect)
        
        # renderizar botones del modal
        self.play_modal_button.render(surf, disabled=not is_unlocked)
        self.close_modal_button.render(surf)