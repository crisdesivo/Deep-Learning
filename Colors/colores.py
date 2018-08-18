#import tensorflow as tf
import numpy as np
import pygame
from pygame.locals import *


rojo=(255, 0, 0)
verde=(0, 255, 0)
azul=(0, 0, 255)
rosa = (255, 0, 255)
celeste = (0, 255, 255)
amarillo = (255, 255, 0)
marron = (150, 75, 9)
violeta = (102, 0, 153)
naranja = (255, 100, 0)
blanco = (255, 255, 255)
gris = (128, 128, 128)
negro = (0, 0, 0)


colores = np.array([rojo, verde, azul, rosa, celeste, amarillo, marron, violeta, naranja, blanco, gris, negro])
pygame.init()
screen=pygame.display.set_mode((500, 500),pygame.RESIZABLE|DOUBLEBUF)
screen_on = True
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 20)
textRojo = myfont.render('Rojo', False, (0, 0, 0))
textAzul = myfont.render('Azul', False, (0, 0, 0))
textVerde = myfont.render('Verde', False, (0, 0, 0))
textRosa = myfont.render('Rosa', False, (0, 0, 0))
textCeleste = myfont.render('Celeste', False, (0, 0, 0))
textAmarillo = myfont.render('Amarillo', False, (0, 0, 0))
textMarron = myfont.render('Marron', False, (0, 0, 0))
textVioleta = myfont.render('Violeta', False, (255, 255, 255))
textNaranja = myfont.render('Naranja', False, (0, 0, 0))
textBlanco = myfont.render('Blanco', False, (0, 0, 0))
textGris = myfont.render('Gris', False, (0, 0, 0))
textNegro = myfont.render('Negro', False, (255, 255, 255))
textColores = np.array([textRojo, textVerde, textAzul, textRosa, textCeleste, textAmarillo, textMarron, textVioleta, textNaranja, textBlanco, textGris, textNegro])



index=0
whiteness = np.random.randint(0, high=255)
r1 = np.random.uniform()
r2 = np.random.uniform()
r3 = (2 - r2 -r1)/2
random_color=(r1*whiteness, r2*whiteness, r3*whiteness)

data= open('coloresData.csv', 'a')
while screen_on:
    pygame.draw.rect(screen, random_color, (0,0, 500, 400))
    for i in range(4):
        for j in range(3):
            pygame.draw.rect(screen, colores[i+4*j], (125*i,400+33*j,125,33))
            screen.blit(textColores[i+4*j], (125*i,400+33*j,125,33))
    pygame.display.flip()

    for event in pygame.event.get():

        if event.type == pygame.KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                screen_on = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.pos[1]>400:
            pos_y=np.int((event.pos[1]-400)/33)
            pos_x=np.int(event.pos[0]/125)
            index = pos_x+pos_y*4
            r, g, b = random_color
            data.write(str(r)+', '+str(g)+', '+str(b)+', '+str(index)+'\n')
            whiteness = np.random.randint(0, high=255)
            r1 = np.random.uniform()
            r2 = np.random.uniform()
            r3 = (2 - r2 -r1)/2
            random_color=(r1*whiteness, r2*whiteness, r3*whiteness)
