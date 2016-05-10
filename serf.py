import pygame
import assets
import entity
import utilities


serf_img = pygame.image.load("art/serf.png")
serf_img.set_colorkey(assets.key)


class Serf(entity.Entity):
    def __init__(self, x, y, current_map):
        super().__init__(x, y, current_map)
        self.image = serf_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 2
        self.change_x = 0
        self.change_y = 0
        self.target = None
        self.health = 30
        self.carry_capacity = 10
        self.name = "Serf"
        self.target = None

    def check_bound(self, current_map):
        if self.rect.left < 20:
            self.rect.left = 20
        if self.rect.right > 1900:
            self.rect.right = 1900
        if self.rect.top < 63:
            self.rect.top = 63
        if self.rect.bottom > 856:
            self.rect.bottom = 856

    def move(self, current_map):
        self.rect.x += self.change_x
        self.collide_x(current_map)
        self.check_bound(current_map)

        self.rect.y += self.change_y
        self.collide_y(current_map)
        self.check_bound(current_map)

    def do_thing(self, current_map):
        if self.target:
            changes = utilities.get_vector(self, self.target[0], self.target[1], self.rect.x + 15, self.rect.y + 22)

            self.change_x = changes[0]
            self.change_y = changes[1]

        self.move(current_map)

    def collide_x(self, current_map):
        serf_hit_list = []
        serf_hit_list = (pygame.sprite.spritecollide(self, current_map.units, False))
        for item in serf_hit_list:
            if self.change_x > 0 and item != self:
                self.rect.right = item.rect.left - 1
            elif self.change_x < 0 and item != self:
                self.rect.left = item.rect.right + 1

    def collide_y(self, current_map):
        serf_hit_list = []
        serf_hit_list = (pygame.sprite.spritecollide(self, current_map.units, False))
        for item in serf_hit_list:
            if self.change_y > 0 and item != self:
                self.rect.right = item.rect.left - 1
            elif self.change_y < 0 and item != self:
                self.rect.left = item.rect.right + 1
