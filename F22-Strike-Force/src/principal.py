from ventana import *

def main(num):
    if num == 1:
        ventjuego = Ventana(800,490,'fondo_menu.png','menu.mp3')

    elif num == 2:
        ventjuego = VentJuego(760, 710, 'fondo_nivel1.png','menu.mp3')

    elif num == 3:
        ventjuego = VentPuntajes(600, 490, 'fondo_menu.png','menu.mp3')

    ventjuego.correr()

def continuar(resp, punt, vidas):
    ventjuego = VentContinuar(600, 360, 'fondo_menu.png','menu.mp3')
    ventjuego.correr(resp, punt, vidas)

if __name__ == '__main__':
    main(1)    
    
    
    




