import os
import random
import pygame, sys, pygame.mixer
from pygame.locals import *
from elementos import *
import juego
from descRecursos import *

class Common:
    def __init__(self):
        self.pygame=0
        self.screen=0

    def ejecutar(self):
        pygame.init()
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((800,490))
        pygame.mouse.set_visible(True)        
        pygame.mixer.set_num_channels(32)
        pygame.display.set_caption("F22 Strike Force")
        screenwidth=screen.get_width()
        screenheight=screen.get_height()
        explosions=0
        return pygame,screen

class ProgressBar():
    def __init__(self):
        common = Common()  
        pygame,self.screen = common.ejecutar()
        
        self.color=(102, 170, 255)
        self.y1 = self.screen.get_height()/2
        self.y2 = self.y1 +20
        self.max_width=800-40
        self.font = pygame.font.Font(CarpetaFuentes + "BITSUMIS.TTF",64)
        self.loading = self.font.render("Cargando", True, self.color)
        self.textHeight=self.y1-80
    def update(self,percent):
        self.screen.fill((0,0,0))
        self.screen.blit(self.loading, (300,self.textHeight))
        txtpercent = self.font.render(str(percent)+"%", True, self.color)
        self.screen.blit(txtpercent, (20,self.y1+30))
        pygame.draw.rect(self.screen, self.color, (20,self.y1,self.max_width,20), 2 )
        pygame.draw.rect(self.screen, self.color, (20,self.y1,(percent*self.max_width)/100,20), 0)
        pygame.display.flip()


class Ventana:
    def __init__(self, width, height, fondo, musica):              
        barra=ProgressBar()
        barra.update(100)
        
        self.texto = Texto(40)
        self.white = (255,255,255)
        self.width = width
        self.height = height
        self.__musica = CarpetaSonidos + musica
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('F22 Strike Force')
        pygame.mixer.init()        
        pygame.mixer.music.load(self.__musica)
        pygame.mixer.music.play()        
        self.imagen=Imagen()
        self.background = self.imagen.cargarImagen(fondo)        
        self.correr()

    def correr(self):
        self.cursor = Cursor()
        self.boton_iniciar = Boton(self.imagen.cargarImagen("boton_iniciar.png"),600,290)
        self.boton_puntajes = Boton(self.imagen.cargarImagen("boton_puntajes.png"),600,350)
        self.boton_salir = Boton(self.imagen.cargarImagen("boton_salir.png"),600,410)
                
        while True:
            self.cursor.actualizar()
            for eventos in pygame.event.get():                
                if eventos.type == QUIT:
                    pygame.mixer.music.stop()
                    pygame.quit()
                    sys.exit()
                elif eventos.type == MOUSEBUTTONDOWN:                    
                    if self.cursor.colliderect(self.boton_iniciar):                        
                        juego.main()
                    if self.cursor.colliderect(self.boton_puntajes):
                        pass
                    if self.cursor.colliderect(self.boton_salir):
                        pygame.mixer.music.stop()
                        pygame.quit()
                        sys.exit()
            self.screen.blit(self.background, (0, 0))            
            self.screen.blit(self.boton_iniciar.imagen, self.boton_iniciar.rect)
            self.screen.blit(self.boton_puntajes.imagen, self.boton_puntajes.rect)
            self.screen.blit(self.boton_salir.imagen, self.boton_salir.rect)
            self.texto.render(self.screen,"F22 Strike Force", self.white ,(400, 0))
            pygame.display.update()
        return 0

class VentJuego(Ventana):
    def correr(self):               
        self.raptor = Raptor(self.imagen)
        self.enemigos = []
        self.enemigo1 = Enemigo(self.imagen)
        self.texto = Texto(25)
        self.balas = []
        self.clock = pygame.time.Clock()
        self.vidas=3
        self.puntaje=0
        while True:
            time = self.clock.tick(60)
            keys = pygame.key.get_pressed()
            for eventos in pygame.event.get():
                if eventos.type == QUIT:
                    pygame.mixer.music.stop()
                    pygame.quit()
                    sys.exit()
            
            if keys[K_SPACE]:               
                x1,x2, y = self.raptor.comprPos()                
                bala1=Bala(x1,y, self.imagen)
                self.balas.append(bala1)
                bala2=Bala(x2,y, self.imagen)
                self.balas.append(bala2)

            self.raptor.mover(time, keys, self.screen)            
            self.enemigo1.actualizar(time, self.raptor)
            self.screen.blit(self.background, (0, 0))            
            for i in range(len(self.balas)):
                if (self.balas[i].actualizar(self.screen)) == True:
                    del(self.balas[i])
                    break
                if self.balas[i].rect.colliderect(self.enemigo1):
                    del(self.balas[i])
                    break   
           
            self.screen.blit(self.raptor.imagen, self.raptor.rect)
            self.screen.blit(self.enemigo1.imagen, self.enemigo1.rect)
            self.texto.render(self.screen, "Puntaje: "+str(self.puntaje), self.white, (0, 0))
            self.texto.render(self.screen, "Vidas: "+str(self.vidas), self.white, (0, 26))
            pygame.display.update()
        return 0


class Imagen:
    def __init__(self):
        pass
    @classmethod
    def cargarImagen(cls, filename, transparent=False):
        filename= CarpetaImagenes + filename
        try: image = pygame.image.load(filename)
        except pygame.error:
            raise SystemExit
        image = image.convert()
        if transparent:
            color = image.get_at((0,0))
            image.set_colorkey(color, RLEACCEL)
        return image

class Boton(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        self.imagen = img
        self.rect = self.imagen.get_rect()
        self.rect.left, self.rect.top = (x, y)

class Cursor(pygame.Rect):        
    def __init__(self):
        pygame.Rect.__init__(self,0,0,1,1)
                
    def actualizar(self):
        self.left, self.top = pygame.mouse.get_pos()

class Texto(pygame.font.Font):
    def __init__(self, FontSize):
        pygame.font.init()
        self.font = pygame.font.Font(CarpetaFuentes + "BITSUMIS.TTF", FontSize)
        self.size = FontSize

    def render(self, surface, text, color, pos):
        x, y = pos
        for i in text.split("z"):
            surface.blit(self.font.render(i, 1, color), (x, y))
            y += self.size


