  #!/usr/bin/env python 
  # -*- coding: utf-8 -*- 

import ventana

def main(num):
    if num == 1:
        ventjuego = ventana.Ventana(800,490,'fondo_menu.png','menu.mp3')

    elif num == 2:
        ventjuego = ventana.VentNivel1(760, 710, 'fondo_nivel1.png','menu.mp3')

    elif num == 3:
        ventjuego = ventana.VentNivel2(760, 710, 'fondo_nivel2.jpg','menu.mp3')

    elif num == 4:
        ventjuego = ventana.VentNivel3(760, 710, 'fondo_nivel1.png','menu.mp3')

    elif num == 5:
        ventjuego = ventana.VentPuntajes(600, 490, 'fondo_menu.png','menu.mp3')

    ventjuego.correr()

def continuar(resp, punt, vidas, nivel):
    ventjuego = ventana.VentContinuar(600, 360, 'fondo_menu.png','menu.mp3')
    ventjuego.correr(resp, punt, vidas, nivel)

if __name__ == '__main__':
    main(1)    
    
    




