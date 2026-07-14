import pygame

# initialise pygame objects
pygame.init()

#  specify screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


#  create pygame screen

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

# set game caption
pygame.display.set_caption('Space invaders')


#  set game icon
gameIcon = pygame.image.load("C:/Users/User/OneDrive/Desktop/GAME/Sprite images/icon.jpg")

pygame.display.set_icon(gameIcon)

PLAYER_WIDTH = 50


# load background images

bg_image = pygame.image.load("C:/Users/User/OneDrive/Desktop/GAME/Sprite images/space2.png")

bg_image = pygame.transform.scale(bg_image,(SCREEN_WIDTH,SCREEN_HEIGHT))

options_image = pygame.image.load("C:/Users/User/OneDrive/Desktop/GAME/Sprite images/options.jpg")
options_image = pygame.transform.scale(options_image,(SCREEN_WIDTH,SCREEN_HEIGHT))