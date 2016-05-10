import pygame
import assets
import entity

tree_img = pygame.image.load("art/tree.png")
tree_img.set_colorkey(assets.key)


class Tree(entity.Entity):
    def __init__(self, x, y, current_map):
        super().__init__(x, y, current_map)
        self.build_image = tree_img
        self.built_image = tree_img
        self.invalid_site_image = tree_img
        self.image = pygame.Surface([30, 30])
        self.image = self.built_image
        self.rect = self.image.get_rect()
        self.current_map = current_map
        self.rect.x = x
        self.rect.y = y
        self.target = None
        self.health = 100
        self.wood = 100
        self.wood_cost = 0
        self.name = "Tree"

