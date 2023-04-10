import pygame, sys
from pygame.locals import QUIT

pygame.init()

# window settings
screen_width = 1401
screen_height = 901

DISPLAYSURF = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Multiprogramming Simulation')


# game variables
TILE_SIZE = 100


# assist functions
def draw_grid():
    for i in range(0,15):
        if i < 10:
            pygame.draw.line(DISPLAYSURF, (255,255,255), (0, i * TILE_SIZE), (screen_width, i * TILE_SIZE))
        pygame.draw.line(DISPLAYSURF, (255,255,255), (i * TILE_SIZE, 0), (i * TILE_SIZE,screen_height))


# load images
# tip: images are loaded from top to bottom.
user_pic = pygame.image.load('images/kontact.svg')

# main loop
while True:

    DISPLAYSURF.blit(user_pic,(100,100))
    draw_grid()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()

