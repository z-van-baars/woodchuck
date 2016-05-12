import assets
import pygame

class GameMap(object):

    def __init__(self):
        self.entity_list = None
        self.background_image = assets.green_background
        self.width = 1880
        self.height = 792
        self.wood = 0
        self.buildings = pygame.sprite.Group()
        self.units = pygame.sprite.Group()
        self.terrain = pygame.sprite.Group()

    def update(self):
    	pass