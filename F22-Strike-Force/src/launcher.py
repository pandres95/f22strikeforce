#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

import ventana 

class Launcher():
    
    def __init__(self): 
        self.window = None    

    def iniciar(self, num, punt=0):      
    
        if num == 1:
            self.window = ventana.VentPrincipal(800,490,'fondo_menu.png','menu.mp3')
            self.window.correr(self)

        elif num == 2:
            self.window = ventana.VentNivel(760, 710, 'fondo_nivel1.png','juego.mp3')
            self.window.inicializar(1, 1, 50, 0.2, [0.2, -0.2], 100,1, 80, 0, 180)
            self.window.correr(self)

        elif num == 3:        
            self.window = ventana.VentNivel(760, 710, 'fondo_nivel2.jpg','juego.mp3')        
            self.window.inicializar(2, 1, 70, 0.5, [0.3, -0.3], 80 ,2, 90, punt, 380)
            self.window.correr(self)        

        elif num == 4:        
            self.window = ventana.VentNivel(760, 710, 'fondo_nivel3.jpg','juego.mp3')
            self.window.inicializar(3, 2, 90, 1, [0.4, -0.4], 60, 3, 100, punt, 730)
            self.window.correr(self)
        
        elif num == 5:
            self.window = ventana.VentNivel(760, 710, 'fondo_nivel4.png','juego.mp3')
            self.window.inicializar(4, 2, 500, 1, [0.2, -0.2], 40, 4, 130, punt, 980)
            self.window.correr(self)

        elif num == 6:
            self.window = ventana.VentPuntajes(600, 490, 'fondo_menu.png','menu.mp3')
            self.window.inicializar()
            self.window.correr(self)

    def continuar(self, resp): 
    
        punt = self.window.puntaje
        vidas = self.window.vidas
        nivel = self.window.nivel  
    
        self.window = ventana.VentContinuar(600, 360, 'fondo_menu.png','menu.mp3')
        self.window.inicializar(resp, punt, vidas, nivel)
        self.window.correr(self)
        

def main():
    launcher = Launcher()
    launcher.iniciar(1)

if __name__ == '__main__':
    main()    
    
    




