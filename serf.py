import pygame
import assets
import entity
import utilities
import sounds
import random
from copy import deepcopy

serf_img = pygame.image.load("art/serf.png")
serf_build_img = pygame.image.load("art/serf_build.png")
serf_invalid_img = pygame.image.load("art/serf_invalid.png")
serf_img.set_colorkey(assets.key)
serf_build_img.set_colorkey(assets.key)
serf_invalid_img.set_colorkey(assets.key)


class Serf(entity.Entity):
    def __init__(self, x, y, current_map):
        super().__init__(x, y, current_map)
        self.invalid_site_image = serf_invalid_img
        self.built_image = serf_img
        self.build_image = serf_build_img
        self.image = serf_build_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 2
        self.change_x = 0
        self.change_y = 0
        self.target = None
        self.target_coords = None
        self.health = 30
        self.max_health = 30
        self.carry_capacity = 10
        self.wood = 0
        self.name = "Serf"
        self.target = None
        self.jobs = ["Idle", "Lumberjack"]
        self.job = 0
        self.current_map = current_map

        # spawn_sound = random.choice(sounds.serf_grunts)
        # pygame.mixer.Sound.play(spawn_sound)

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
        # self.collide_x(current_map)
        self.check_bound(current_map)

        self.rect.y += self.change_y
        # self.collide_y(current_map)
        self.check_bound(current_map)

    def lumberjack(self):
        if self.wood >= self.carry_capacity:
            # drop off load of wood at gather point
            pass
        if self.wood < self.carry_capacity:
            # keep lumberjacking / move to target tree
            pass
        if self.wood == 0:
            # return to target tree
            pass

    def no_profession(self):
        if self.target_coords is not None:
            changes = utilities.get_vector(self, self.target_coords[0], self.target_coords[1], self.rect.x + 15, self.rect.y + 22)
            self.change_x = changes[0]
            self.change_y = changes[1]
            if not self.collide_check():
                self.move(self.current_map)

    def collide_check(self):
        # hypothetical copy of ourself
        projection = pygame.sprite.Sprite()
        projection.image = self.image
        projection.rect = deepcopy(self.rect)

        # hypothetically move where we want to go
        projection.rect.x += self.change_x * 2
        projection.rect.y += self.change_y * 2 

        # do we have any collisions?
        future_collisions = []
        for unit in self.current_map.units:
            if projection.rect.colliderect(unit.rect):
                future_collisions.append(unit)

        while self in future_collisions: future_collisions.remove(self)
        if future_collisions:
            distances_to_collision = map(self.remaining_distance, future_collisions)
            # type: Iterable[Tuple[int, int]]

            x_changes, y_changes = zip(*distances_to_collision)
            # type: Iterable[int]
            # type: Iterable[int]

            self.change_x = utilities.abs_min(x_changes)
            self.change_y = utilities.abs_min(y_changes)
            return True
        else:
            # no collisions, good to go!
            return False

    def remaining_distance(self, obstacle):
        buffer = 2
        if self.change_x > 0:  # heading to the right
            leading_edge = self.rect.right + buffer
            remaining_x = obstacle.rect.left - leading_edge

        elif self.change_x <= 0:  # heading to the left
            leading_edge = self.rect.left - buffer
            remaining_x = leading_edge - obstacle.rect.right

        if self.change_y > 0:  # heading down
            leading_edge = self.rect.bottom + buffer
            remaining_y = obstacle.rect.top - leading_edge

        elif self.change_y <= 0:
            leading_edge = self.rect.top - buffer
            remaining_y = leading_edge - obstacle.rect.bottom

        return (remaining_x, remaining_y)

    def do_thing(self, current_map):
        if self.job == 0:
            self.no_profession()
        if self.job == 1:
            self.lumberjack()

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
