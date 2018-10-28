import math, random, sys
import pygame
from pygame.locals import *

# exit the program
def events():
	for event in pygame.event.get():
		if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
			pygame.quit()
			sys.exit()

# define display surface			
W, H = 1024, 576
HW, HH = W / 2, H / 2
AREA = W * H

# initialise display
pygame.init()
CLOCK = pygame.time.Clock()
DS = pygame.display.set_mode((W, H))
pygame.display.set_caption("code.Pylet - Template")
FPS = 120

# define some colors
BLACK = (0, 0, 0, 255)
WHITE = (255, 255, 255, 255)
bkgd = pygame.image.load("mountains.png").convert()
grass = pygame.image.load("grass.png").convert()
y = 0

# main loop
while True:
	events()
	rel_y = y % bkgd.get_rect().height
	
	DS.blit(bkgd,(0,rel_y - bkgd.get_rect().height))
	if rel_y < H:
    		DS.blit(bkgd,(0,rel_y))
	
	y = y-1
	''' rel_x = x % bkgd.get_rect().width
	DS.blit(bkgd,(rel_x - bkgd.get_rect().width,0))
	
	if rel_x < W:
    		DS.blit(bkgd, (rel_x,0))
	x-=1 '''


	pygame.display.update()
	CLOCK.tick(FPS)
	DS.fill(BLACK)