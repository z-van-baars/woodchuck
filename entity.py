import assets
import pygame

class Entity(pygame.sprite.Sprite):
    def __init__(self, x, y, current_map, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y