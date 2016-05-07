import assets
import pygame


class Entity(pygame.sprite.Sprite):
    def __init__(self, x, y, current_map):
        super().__init__()