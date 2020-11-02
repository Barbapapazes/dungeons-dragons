import pygame
import pygame_widgets as pw
from menu_class import *

pygame.init()
surface= pygame.display.set_mode((1024,768))

image=pygame.image.load("background.jpg").convert()
image=pygame.transform.scale(image,(1024,768))


titre=police.render("LE TITRE DU JEU ",True,pygame.Color(255,255,255))



Mp=classe_Menu_prin()
continuer = True

while continuer:
    surface.blit(image,(0,0))
    surface.blit(titre,(250,20))

    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            continuer = False

    Mp.affichage(event)
    pygame.display.flip()

pygame.quit()