#!/usr/bin/env python

import sys, pygame
from pygame.locals import *
import random
from copy import copy

width=760
height=710

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
        if self.rect.bottom <= height:
            if keys[K_DOWN]:
                self.rect.centery += self.speed * time
        if self.rect.right <= width:
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
    def __init__(self, im, num, speed, vida):
        pygame.sprite.Sprite.__init__(self)
        self.num = num        
        self.imagen = im.cargarImagen("enemigo"+str(num)+".png", True)        
        self.rect = self.imagen.get_rect()
        if self.num != 4:
            self.rect.centerx = random.randint(64, width-20)
            self.rect.centery = random.randint(64, height/ 2)
        else:
            self.rect.centerx = 400
            self.rect.centery = 150
        self.speed = speed
        self.vida = vida        

    def actualizar(self, time):                        
        self.rect.centerx += self.speed[0] * time
        if self.num != 4:
            self.rect.centery += self.speed[1] * time       
            
        if self.rect.left <= 10 or self.rect.right >= width:
            self.speed[0] = -self.speed[0]
            self.rect.centerx += self.speed[0] * time
        if self.num != 4:
            if self.rect.top <= 0 or self.rect.bottom >= height/2:
                self.speed[1] = -self.speed[1]
                self.rect.centery += self.speed[1] * time

    def detColision(self, time, objeto):
        if pygame.sprite.collide_rect(self, objeto):
            self.speed[0] = -self.speed[0]
            self.rect.centerx += self.speed[0] * time

    def comprPos(self):
        x = self.rect.centerx         
        y = self.rect.centery - 20
        return x,y
     
    def clone(self):
        obj = copy(self)        
        return obj        


class Bala(pygame.sprite.Sprite):       
    def __init__(self, x, y, im):
        pygame.sprite.Sprite.__init__(self)
        self.imagen = im.cargarImagen("bala.png", True)
        self.rect = self.imagen.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = 20
                
    def actualizar(self, objeto):        
        if (self.rect.centery+20)<0:
            x = True        
        else:
            self.rect.centery -= self.speed            
            x = False
    
        if pygame.sprite.collide_rect(self, objeto):
            y = True
        else:            
            y = False
        
        return x, y

class BalaEnemigo(Bala):
    def __init__(self, x, y, im, num):
        pygame.sprite.Sprite.__init__(self)        
        self.imagen = im.cargarImagen("disparo"+str(num)+".png", True)
        self.rect = self.imagen.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = 9
        
    def actualizar(self, objeto):                
        if (self.rect.centery+20)>height:
            x = True        
        else:
            self.rect.centery += self.speed                   
            x = False      
        
        if pygame.sprite.collide_rect(self, objeto):
            y = True
        else:            
            y = False           
        
        return x, y

class Bonus(pygame.sprite.Sprite):       
    def __init__(self, im, imagen):
        pygame.sprite.Sprite.__init__(self)
        self.imagen = im.cargarImagen(imagen, True)
        self.rect = self.imagen.get_rect()
        self.rect.centerx = random.randint(20, width-20)
        self.rect.centery = random.randint(90, height-20)
        self.speed = [0.08, -0.08]

    def actualizar(self, time):                  
        self.rect.centerx += self.speed[0] * time
        self.rect.centery += self.speed[1] * time       
            
        if self.rect.left <= 0 or self.rect.right >= width:
            self.speed[0] = -self.speed[0]
            self.rect.centerx += self.speed[0] * time
        if self.rect.top <= 121 or self.rect.bottom >= height:
            self.speed[1] = -self.speed[1]
            self.rect.centery += self.speed[1] * time

    def detColision(self, time, raptor):
        if pygame.sprite.collide_rect(self, raptor):
            return True
        else:
            return False
