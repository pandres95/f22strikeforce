#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

import ventana

def main(num, punt=0):
    if num == 1:
        ventjuego = ventana.Ventana(800,490,'fondo_menu.png','menu.mp3')
        ventjuego.correr()

    elif num == 2:
        ventjuego = ventana.VentNivel(760, 710, 'fondo_nivel1.png','menu.mp3')
        ventjuego.correr(1, 1, 50, 0.2, [0.2, -0.2], 100,1, 100, 0, 300)

    elif num == 3:        
        ventjuego = ventana.VentNivel(760, 710, 'fondo_nivel2.jpg','menu.mp3')        
        ventjuego.correr(2, 1, 70, 0.5, [0.3, -0.3], 80 ,2, 210, punt, 600)

    elif num == 4:        
        ventjuego = ventana.VentNivel(760, 710, 'fondo_nivel3.jpg','menu.mp3')
        ventjuego.correr(3, 2, 90, 1, [0.4, -0.4], 60, 3, 320, punt, 850)

    elif num == 5:
        ventjuego = ventana.VentPuntajes(600, 490, 'fondo_menu.png','menu.mp3')
        ventjuego.correr()

def continuar(resp, punt, vidas, nivel): 
    ventjuego = ventana.VentContinuar(600, 360, 'fondo_menu.png','menu.mp3')
    ventjuego.correr(resp, punt, vidas, nivel)

if __name__ == '__main__':
    main(1)    
    
    




