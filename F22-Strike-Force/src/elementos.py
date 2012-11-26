#!/usr/bin/env python

import sys, pygame
from pygame.locals import *
from ventana import *
import random

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
    def __init__(self, im, num):
        pygame.sprite.Sprite.__init__(self)
        self.imagen = im.cargarImagen("enemigo"+str(num)+".png", True)
        self.rect = self.imagen.get_rect()
        self.rect.centerx = random.randint(64, WIDTH-20)
        self.rect.centery = random.randint(64, HEIGHT/ 2)
        self.speed = [0.3, -0.3]
        self.vida = 50        

    def actualizar(self, time):                  
        self.rect.centerx += self.speed[0] * time
        self.rect.centery += self.speed[1] * time       
            
        if self.rect.left <= 10 or self.rect.right >= WIDTH:
            self.speed[0] = -self.speed[0]
            self.rect.centerx += self.speed[0] * time
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT/2:
            self.speed[1] = -self.speed[1]
            self.rect.centery += self.speed[1] * time

    def detColision(self, time, objeto):
        if pygame.sprite.collide_rect(self, objeto):
            self.speed[0] = -self.speed[0]
            self.rect.centerx += self.speed[0] * time

    def comprPos(self):
        x1 = self.rect.centerx + 15
        x2 = self.rect.centerx - 15
        y = self.rect.centery - 20
        return x1,x2,y
        

class Bala(pygame.sprite.Sprite):       
    def __init__(self, x, y, im):
        pygame.sprite.Sprite.__init__(self)
        self.imagen = im.cargarImagen("bala.png", True)
        self.rect = self.imagen.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = [20, -20]
                
    def actualizar(self):        
        if (self.rect.centery+20)<0:
            return True        
        else:
            self.rect.centery -= self.speed[0]            
            return False

    def detColision(self, objeto):
        if pygame.sprite.collide_rect(self, objeto):
            return True
        else:
            return False

class BalaEnemigo(Bala):
    def __init__(self, x, y, im):
        pygame.sprite.Sprite.__init__(self)
        self.imagen = im.cargarImagen("disparo1.png", True)
        self.rect = self.imagen.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = [9, -9]
        
    def actualizar(self):        
        if (self.rect.centery+20)>HEIGHT:
            return True        
        else:
            self.rect.centery += self.speed[0]            
            return False

class Bonus(pygame.sprite.Sprite):       
    def __init__(self, im, imagen):
        pygame.sprite.Sprite.__init__(self)
        self.imagen = im.cargarImagen(imagen, True)
        self.rect = self.imagen.get_rect()
        self.rect.centerx = random.randint(20, WIDTH-20)
        self.rect.centery = random.randint(90, HEIGHT-20)
        self.speed = [0.08, -0.08]

    def actualizar(self, time):                  
        self.rect.centerx += self.speed[0] * time
        self.rect.centery += self.speed[1] * time       
            
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.speed[0] = -self.speed[0]
            self.rect.centerx += self.speed[0] * time
        if self.rect.top <= 121 or self.rect.bottom >= HEIGHT:
            self.speed[1] = -self.speed[1]
            self.rect.centery += self.speed[1] * time

    def detColision(self, time, raptor):
        if pygame.sprite.collide_rect(self, raptor):
            return True
        else:
            return False
