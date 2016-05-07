import pygame
import assets
import entity

serf_img = pygame.image.load("art/serf.png")
serf_img.set_colorkey(assets.key)

class Serf(entity.Entity):
    def __init__(self, x, y, current_map):
        super().__init__()
        self.image = serf_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 2
        self.change_x = 0
        self.change_y = 0
        self.target = None
