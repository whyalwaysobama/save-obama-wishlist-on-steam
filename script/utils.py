import os

import pygame

BASE_IMG_PATH = 'img/'

def load_image(path, scale=None):
    img = pygame.image.load(BASE_IMG_PATH + path).convert()

    if scale :
        img = pygame.transform.scale(img, scale)
    if path == "Niveles/Niveles sin sida.png" :
        return img
    if path == 'logo.jpg':
        img.set_colorkey((255, 255, 255))
        return img
    if "Niveles" in path :
        return img
    else:   
        img.set_colorkey((0, 0, 0))
    return img
    # carga una imagen con la escala dada y le saca el fondo

def load_images(path, scale=None):
    images = []
    full_path = os.path.join(BASE_IMG_PATH, path)

    for img_name in os.listdir(full_path):
        img_path = os.path.join(path, img_name)
        images.append(load_image(img_path, scale))

    return images
    # carga una lista de imagenes con la escala dada y les saca el fondo

class Animation :
    def __init__ (self, images, img_dur = 5, loop = True) :
        self.images = images
        self.loop = loop
        self.dur = img_dur
        self.done = False
        self.frame = 0
    
    def copy (self) :
        return Animation (self.images, self.dur, self.loop)
    
    def update (self) :
        if self.loop :
            self.frame = (self.frame + 1) % (self.dur * len(self.images))
        else:
            self.frame = min (self.frame + 1, self.dur * len (self.images) - 1)
            if self.frame >= self.dur * len (self.images) - 1:
                self.done = True
        
    def img(self) :
        return self.images[int(self.frame / self.dur)]  