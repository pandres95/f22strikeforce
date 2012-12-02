#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

from pygame import *
from elementos import *
from principal import *
try:
    import cPickle as pickle
except:
    import pickle

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
        self.font = pygame.font.Font("../res/fonts/BITSUMIS.TTF",64)
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
        self.texto = Texto(40)
        self.white = (255,255,255)
        self.width = width
        self.height = height
        self.__musica = '../res/sounds/'+musica
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('F22 Strike Force')
        pygame.mixer.init()        
        pygame.mixer.music.load(self.__musica)
        pygame.mixer.music.play()        
        self.imagen=Imagen()
        self.background = self.imagen.cargarImagen(fondo)       

    def correr(self):
        barra=ProgressBar()
        barra.update(100)
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
                        main(2)
                    if self.cursor.colliderect(self.boton_puntajes):
                        main(5)
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

class VentNivel(Ventana):
    def correr(self, n_enemigo, bala_enem, vida_enemigo, vid_rest_raptor, vel_enem, contador, nivel, puntaje):           
        self.sonDisparo = pygame.mixer.Sound("../res/sounds/disparo.wav") 
        self.sonDisparo.set_volume(0.2)
        self.sonLaser = pygame.mixer.Sound("../res/sounds/laser.wav") 
        self.sonLaser.set_volume(0.2)
        self.sonExplos1 = pygame.mixer.Sound("../res/sounds/explosion1.wav") 
        self.sonExplos1.set_volume(0.1)           
        self.raptor = Raptor(self.imagen)        
        self.numEnemigos = 1
        self.enemigos = []
        enemigo = Enemigo(self.imagen, n_enemigo) 
        enemigo.vida = vida_enemigo
        enemigo.speed = vel_enem     
        self.enemigos.append(enemigo)        
        self.texto = Texto(25)
        self.balas = []
        self.balasEnem = []
        self.clock = pygame.time.Clock()
        self.vidas = 3
        self.puntaje = 0
        self.contador1 = 0
        self.contador2 = 0
        self.nBonusVida = False
                
        while True:         
                       
            #Muestra ventana de nivel perdido
            
            if self.vidas <= 0:
                continuar(False, self.puntaje, self.vidas, nivel) 
            
            #Muestra ventana de nivel superado
                
            if self.puntaje >= puntaje:
                continuar(True, self.puntaje, self.vidas, nivel) 
            
            self.contador1 += 1
            self.contador2 += 1
            
            if self.contador1 == contador+1:
                self.contador1 = 1

            if self.contador2 == 2101:
                self.contador2 = 1
                self.nBonusVida = False
                self.BonusVida = 0
                
            time = self.clock.tick(45)
            keys = pygame.key.get_pressed()
            for eventos in pygame.event.get():
                if eventos.type == QUIT:
                    pygame.mixer.music.stop()
                    pygame.quit()
                    sys.exit()

            #Mostrar la venta Continuar
            
            if keys[K_ESCAPE]:      
                continuar(False, self.puntaje, self.vidas, nivel)  
                
            #Crear balas de raptor       
            
            if keys[K_SPACE]:               
                x1,x2, y = self.raptor.comprPos()                
                bala1=Bala(x1,y, self.imagen)
                self.balas.append(bala1)
                bala2=Bala(x2,y, self.imagen)
                self.balas.append(bala2)                
                self.sonDisparo.play()

            #Crear balas de enemigos

            if self.contador1 == contador:
                for i in range(len(self.enemigos)):
                    x1,x2, y = self.enemigos[i].comprPos()                
                    bala1=BalaEnemigo(x1,y, self.imagen, bala_enem)
                    self.balasEnem.append(bala1)
                    bala2=BalaEnemigo(x2,y, self.imagen, bala_enem)
                    self.balasEnem.append(bala2)  
                    self.sonLaser.play()               
                              

            #Crear bonus de vida

            if self.contador2 == 2000:
                self.nBonusVida = True
                self.BonusVida = Bonus(self.imagen, "lifebonus.png")
                
            #Crea más enemigos cuando ya no queda ninguno

            if (len(self.enemigos)) == 0:
                self.numEnemigos += 1                
                for i in range(self.numEnemigos):
                    enemigo = Enemigo(self.imagen, n_enemigo)   
                    enemigo.vida = vida_enemigo     
                    enemigo.speed = vel_enem
                    self.enemigos.append(enemigo)               
                          
            
            #Crea el bonus de vida
            
            if self.nBonusVida == True:                 
                self.BonusVida.actualizar(time)
            
            self.raptor.mover(time, keys, self.screen)
            
            #Detectar colisión de bonus de vida con el raptor

            if self.nBonusVida == True:
                if self.BonusVida.detColision(time, self.raptor) == True:
                    self.contador2 = 1
                    self.nBonusVida = False
                    self.BonusVida = 0
                    self.vidas += 1          
                    
            #Actualiza los enemigos y detecta colisiones entre enemigos y el raptor
            
            for i in range(len(self.enemigos)):
                self.enemigos[i].actualizar(time)
                self.enemigos[i].detColision(time, self.raptor)               
                                
            #Actualiza colisiones entre enemigos

            for i in range(len(self.enemigos)):
                for j in range(len(self.enemigos)):
                    if i != j:
                        self.enemigos[i].detColision(time, self.enemigos[j])
                        
            #Borra enemigos que pierden todas sus vidas

            for j in range(len(self.enemigos)):
                if self.enemigos[j].vida <= 0:
                    del(self.enemigos[j])
                    break                        
                
            #Detecta colisiones entre balas y raptor

            for j in range(len(self.balasEnem)):
                x, y = self.balasEnem[j].actualizar(self.raptor)
                if y == True:                     
                    self.vidas -= vid_rest_raptor
                    self.sonExplos1.play()
                if x == True or y == True:
                    del(self.balasEnem[j])
                    break                    

            
            #Borra balas que se salen de la ventana

            for i in range(len(self.enemigos)):
                for j in range(len(self.balas)):                
                    x, y = self.balas[j].actualizar(self.enemigos[i])
                    if y == True:                     
                        self.enemigos[i].vida -= 1
                        self.puntaje += 0.5
                        self.sonExplos1.play()     
                    if x == True or y == True:
                        del(self.balas[j])
                        break                     

            #MOSTRAR OBJETOS EN PANTALLA    
                
            self.screen.blit(self.background, (0, 0))               
                    
            if self.nBonusVida == True:                
                self.screen.blit(self.BonusVida.imagen, self.BonusVida.rect)            
            
            for i in range(len(self.enemigos)):
                self.screen.blit(self.enemigos[i].imagen, self.enemigos[i].rect)  
                
            for i in range(len(self.balas)):
                self.screen.blit(self.balas[i].imagen, self.balas[i].rect)  
                
            for i in range(len(self.balasEnem)):
                self.screen.blit(self.balasEnem[i].imagen, self.balasEnem[i].rect)            

            self.screen.blit(self.raptor.imagen, self.raptor.rect)            
            self.texto.render(self.screen, "Puntaje: "+str(int(self.puntaje)), self.white, (0, 0))
            
            impresion = 0
            if self.vidas > int(self.vidas):
                impresion = int(self.vidas) + 1
            elif self.vidas == int(self.vidas):
                impresion = int(self.vidas)
            self.texto.render(self.screen, "Vidas: "+str(impresion), self.white, (0, 26))
            
            pygame.display.update()
        return 0

class VentPuntajes(Ventana):
    def correr(self):
        self.texto = Texto(35)    
        self.texto2 = Texto(25)    
        self.cursor = Cursor()        
        self.boton_regresar = Boton(self.imagen.cargarImagen("boton_regresar.png"),330,420)
        self.boton_salir = Boton(self.imagen.cargarImagen("boton_salir.png"),130,420)
        
        self.fichero = Fichero()
        self.puntFichero = []
        self.num = []
        linea = ""
        for i in range(3):
            linea = self.fichero.mostrarPunt(i)
            self.puntFichero.append(linea)              
            
        self.impresion = []
            
        for i in range(3):              
            if self.puntFichero[i] != 0:                 
                self.num.append(str(i+1)+".")
                self.impresion.append(str(self.puntFichero[i]))
            else:
                self.num.append("")
                self.impresion.append("")
                
        while True:
            self.cursor.actualizar()
            for eventos in pygame.event.get():                
                if eventos.type == QUIT:
                    pygame.mixer.music.stop()
                    pygame.quit()
                    sys.exit()
                elif eventos.type == MOUSEBUTTONDOWN:                    
                    if self.cursor.colliderect(self.boton_regresar):
                        main(1)
                    if self.cursor.colliderect(self.boton_salir):
                        pygame.mixer.music.stop()
                        pygame.quit()
                        sys.exit()
            self.screen.blit(self.background, (0, 0))            
            self.screen.blit(self.boton_regresar.imagen, self.boton_regresar.rect)
            self.screen.blit(self.boton_salir.imagen, self.boton_salir.rect)
            self.texto.render(self.screen,"Puntajes", self.white ,(200, 30))                       
           
            self.texto2.render(self.screen,"Mas altos:   "+self.num[0]+"   "+self.impresion[0], self.white ,(40, 200))   
            self.texto2.render(self.screen,"              "+self.num[1]+"   "+self.impresion[1], self.white ,(40, 250))
            self.texto2.render(self.screen,"              "+self.num[2]+"   "+self.impresion[2], self.white ,(40, 300))  
                       
            pygame.display.update()
        return 0
    
class VentContinuar(Ventana):
    def correr(self, resp, punt, vidas, nivel):
        self.texto = Texto(35)   
        self.texto2 = Texto(25)      
        self.cursor = Cursor()   
        if resp == True:
            x1 = 50
            x2 = 231
        else:
            x1 = 160
            x2 = 320
        self.boton_salir = Boton(self.imagen.cargarImagen("boton_salir.png"),x1,300)
        self.boton_menu = Boton(self.imagen.cargarImagen("boton_menu.png"),x2,300)
        if resp == True:
            self.boton_siguiente = Boton(self.imagen.cargarImagen("boton_siguiente.png"),410,300)
            
        self.fichero = Fichero()
        if punt != 0:
            self.fichero.agregarPunt(int(punt)) 
                
        while True:
            self.cursor.actualizar()
            for eventos in pygame.event.get():                
                if eventos.type == QUIT:
                    pygame.mixer.music.stop()
                    pygame.quit()
                    sys.exit()
                elif eventos.type == MOUSEBUTTONDOWN:                    
                    if self.cursor.colliderect(self.boton_menu):
                        main(1)
                    if self.cursor.colliderect(self.boton_salir):
                        pygame.mixer.music.stop()
                        pygame.quit()
                        sys.exit()
                    if resp == True:
                        if self.cursor.colliderect(self.boton_siguiente):                            
                            main(nivel+2)
                    
            self.screen.blit(self.background, (0, 0))        
            self.screen.blit(self.boton_salir.imagen, self.boton_salir.rect)    
            self.screen.blit(self.boton_menu.imagen, self.boton_menu.rect)
            if resp == True:
                self.screen.blit(self.boton_siguiente.imagen, self.boton_siguiente.rect)
            if resp == True:
                text = "superado"
                y = 140
            else:
                text = "no superado"               
                y = 115
            self.texto.render(self.screen,"Nivel "+text, self.white ,(y, 30))
            self.texto2.render(self.screen,"Puntaje:   "+str(int(punt)), self.white ,(20, 130))
            impresion = 0
            if vidas > int(vidas):
                impresion = int(vidas) + 1
            elif vidas == int(vidas):
                impresion = int(vidas)
            self.texto2.render(self.screen,"Vidas:      "+str(impresion), self.white ,(20, 170))
            pygame.display.update()
        return 0
        

class Imagen:
    def __init__(self):
        pass
    @classmethod
    def cargarImagen(cls, filename, transparent=False):
        filename = '../res/images/' + filename
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
        self.font = pygame.font.Font("../res/fonts/BITSUMIS.TTF", FontSize)
        self.size = FontSize

    def render(self, surface, text, color, pos):
        x, y = pos
        for i in text.split("z"):
            surface.blit(self.font.render(i, 1, color), (x, y))
            y += self.size

class Fichero():
    def __init__(self):
        try:
            self.punt = pickle.load(open("puntajes.txt", "rb"))
        except:
            self.punt = [0,0,0]
        
    def guardar(self):
        try:
            pickle.dump(self.punt, open("puntajes.txt", "wb"))
        except:
            print("Error: tu pinche archivito no está guardando")
                             
        
    def agregarPunt(self, puntaje):        
        compr = False
        for i in range(len(self.punt)):
            if self.punt[i] == puntaje:
                compr = True
                
        if compr == False:
            self.punt.append(puntaje)
            self.punt.sort()
            self.punt.reverse()           
            tmp = []
            for i in range(3):
                tmp.append(self.punt[i])
            self.punt = tmp            
            self.guardar()
        
    def mostrarPunt(self, i):
        return self.punt[i]
