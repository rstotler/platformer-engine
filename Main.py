import pygame, Game
from pygame import *

pygame.init()
window = pygame.display.set_mode((1280,720),0,32)
pygame.display.set_caption("Platformer Engine 0.0915")
clock = pygame.time.Clock()
game = Game.Load(window)

while True:

	dt = clock.tick(60)
	game.Update(window,clock,dt/1000.)
	pygame.display.flip()
	