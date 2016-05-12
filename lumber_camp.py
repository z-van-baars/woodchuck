import pygame
import assets
import entity
import serf

lumber_camp_img = pygame.image.load("art/lumber_camp.png")
lumber_camp_build_img = pygame.image.load("art/lumber_camp_build.png")
lumber_camp_invalid_img = pygame.image.load("art/lumber_camp_invalid.png")
lumber_camp_img.set_colorkey(assets.key)
lumber_camp_build_img.set_colorkey(assets.key)
lumber_camp_invalid_img.set_colorkey(assets.key)


class LumberCamp(entity.Entity):
    def __init__(self, x, y, current_map):
        super().__init__(x, y, current_map)
        self.build_image = lumber_camp_build_img
        self.built_image = lumber_camp_img
        self.invalid_site_image = lumber_camp_invalid_img
        self.image = pygame.Surface([60, 60])
        self.image = self.build_image
        self.rect = self.image.get_rect()
        self.current_map = current_map
        self.rect.x = x
        self.rect.y = y
        self.target = None
        self.health = 1000
        self.max_health = 1000
        self.wood_cost = 50
        self.name = "Lumber Camp"

    def valid_build_site(self):

        collisions = pygame.sprite.Group()
        collisions = (pygame.sprite.spritecollide(self, self.current_map.buildings, False))

        if collisions:
            self.image = self.invalid_site_image
        else:
            self.image = self.build_image

        return collisions

    def event_processing(self, event):
        pass

    def spawn_serf(self):
        new_serf = serf.Serf(self.rect.x + 60, self.rect.y + 60, self.current_map)
        pass

    def build(self, pos):
        pygame.mouse.set_visible(0)
        self.rect.x = pos[0]
        self.rect.y = pos[1]

