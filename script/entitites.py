import pygame

class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0] 
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False} # colisiones en cada direccion
        self.action = ''
        self.anim_offset = (-3, -3)
        self.flip = False
        self.set_action ('idle')
        self.anim_offset = (0,0)

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1]) # funcion para hacer mas rapido
        
    def set_action (self, action) :
        if action != self.action :
            self.action = action
            self.animation = self.game.assets [self.type + '/' + self.action].copy()

    def update(self, tilemap, movement=(0, 0)):
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
        
        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])
        # aplicar movimiento en pixeles
        self.pos[0] += frame_movement[0]
        entity_rect = self.rect() # el rect de la entidad
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0:
                    entity_rect.right = rect.left
                    self.collisions['right'] = True
                if frame_movement[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions['left'] = True
                self.pos[0] = entity_rect.x
                # movimiento hasta q detecte una colision q lo frene en el eje x
        
        self.pos[1] += frame_movement[1]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                if frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                self.pos[1] = entity_rect.y
        # lo mismo pero en y
        
        if movement [0] > 0 :
            self.flip = False
        if movement [0] < 0 :
            self.flip = True     

        self.velocity[1] = min(5, self.velocity[1] + 0.1)
        # gravedad
        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0 
        # si se choca con el piso o el techo se frena la velocidad en y
        
        self.animation.update ()

    def render(self, surf, offset = (0,0)):
       surf.blit(pygame.transform.flip(self.animation.img(), self.flip, False), (self.pos [0] - offset [0] + self.anim_offset[0], self.pos [1] - offset [1] + self.anim_offset[1]))
      
class Player(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, 'player', pos, size) 
        self.air_time = 0
        self.animation_locked = False
        self.dashing = False
        self.dash_time = 0
        self.dash_cooldown = 0  # Nuevo: cooldown del dash

    def update(self, tilemap, movement=(0, 0), clicking=False):
        # Reducir el cooldown cada frame
        if self.dash_cooldown > 0:
            self.dash_cooldown -= 1
        
        # Si está haciendo el dash
        if self.dashing:
            dash_direction = -1 if self.flip else 1
            movement = (dash_direction * 1.5, movement[1])
            
            # Control del arco según el tiempo del dash
            if self.dash_time < 5:
                self.velocity[1] = -2.5
            elif self.dash_time < 12:
                self.velocity[1] = -0.5
            
            self.dash_time += 1
        
        super().update(tilemap, movement=movement) 
        self.air_time += 1

        if self.collisions['down']:
            self.air_time = 0
            if self.dashing:
                self.animation_locked = False
                self.dashing = False
                self.dash_time = 0
                return
        
        if self.dashing:
            return
        
        if self.animation_locked:
            if self.animation.done:
                self.animation_locked = False
                self.dashing = False
                self.dash_time = 0
            else:
                return
        
        # Solo puede dashear si no está en cooldown
        if clicking and self.dash_cooldown == 0:
            self.set_action("save")
            self.animation_locked = True
            self.dashing = True
            self.dash_time = 0
            self.dash_cooldown = 60  # 60 frames = 1 segundo (ajustá esto)
        elif self.air_time > 4: 
            self.set_action('jump')
        elif movement[0] != 0: 
            self.set_action('run')
        else: 
            self.set_action('idle')