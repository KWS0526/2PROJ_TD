import pygame
from src.componant.game import Map

if __name__ == '__main__':
    pygame.init()
    maps = Map()
    maps.run()