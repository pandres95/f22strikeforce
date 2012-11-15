#!/usr/bin/env python

import sys, pygame
from pygame.locals import *
from ventana import *

WIDTH=760
HEIGHT=710

class Raptor(pygame.sprite.Sprite):
    def __init__(self, im):
        pygame.sprite.Sprite.__init__(self)
        self.imagen = im.cargarImagen("raptor.png", True)
        self.rect = self.imagen.get_rect()
        self.rect.centerx = 360
        self.rect.centery = 610
        self.speed = 0.6

    def mover(self, time, keys, screen):
        if keys[K_ESCAPE]:
            pygame.quit()
            sys.exit()       
            
        if self.rect.top >= 0:
            if keys[K_UP]:
                self.rect.centery -= self.speed * time
        if self.rect.bottom <= HEIGHT:
            if keys[K_DOWN]:
                self.rect.centery += self.speed * time
        if self.rect.right <= WIDTH:
            if keys[K_RIGHT]:
                self.rect.centerx += self.speed * time
        if self.rect.left > 0:
            if keys[K_LEFT]:
                self.rect.centerx -= self.speed * time

    def comprPos(self):
        x1 = self.rect.centerx + 15
        x2 = self.rect.centerx - 15
        y = self.rect.centery - 20
        return x1,x2,y

class Enemigo(pygame.sprite.Sprite):
    def __init__(self, im):
        pygame.sprite.Sprite.__init__(self)
        self.imagen = im.cargarImagen("enemigo.png", True)
        self.rect = self.imagen.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.centery = HEIGHT / 2
        self.speed = [0.3, -0.3]

    def actualizar(self, time, raptor):
        self.rect.centerx += self.speed[0] * time
        self.rect.centery += self.speed[1] * time
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.speed[0] = -self.speed[0]
            self.rect.centerx += self.speed[0] * time
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT/2:
            self.speed[1] = -self.speed[1]
            self.rect.centery += self.speed[1] * time

        if pygame.sprite.collide_rect(self, raptor):
              self.speed[0] = -self.speed[0]
              self.rect.centerx += self.speed[0] * time

class Bala(pygame.sprite.Sprite):       
    def __init__(self, x, y, im):
        pygame.sprite.Sprite.__init__(self)
        self.imagen = im.cargarImagen("bala.png", True)
        self.rect = self.imagen.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = [5, -5]
                
    def actualizar(self, screen):        
        if (self.rect.centery+30)<0:
            return True        
        else:
            self.rect.centery -= self.speed[0]
            screen.blit(self.imagen, self.rect)
            return False
