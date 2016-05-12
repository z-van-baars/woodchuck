import assets
import pygame
import math


class Entity(pygame.sprite.Sprite):
    def __init__(self, x, y, current_map):
        super().__init__()
        self.health_box = None

    def do_thing(self, current_map):
        pass

class HealthBox(pygame.sprite.Sprite):
    def __init__(self, x, y, current_health, max_health):
        super().__init__()
        self.image = pygame.Surface([20, 2])
        self.rect = self.image.get_rect()
        self.image.fill(assets.red)
        self.rect.x = 0
        self.rect.y = 0
        self.max_health = max_health
        self.current_health = current_health

    def get_health_pixels(self, current_health):
        self.current_health = current_health
        health_percentage = round(self.current_health / self.max_health)
        out_of_twenty = round(health_percentage / 5)
        self.image.fill(assets.green)

    def get_new_position(self, x, y, x_adjust):
        x_adjust = x_adjust - 20
        x_adjust = x_adjust / 2
        x_adjust = round(x_adjust)
        self.rect.x = x + x_adjust
        self.rect.y = y - 8
