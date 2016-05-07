import pygame
import assets
import entity

lumber_camp_img = pygame.image.load("art/lumber_camp.png")
lumber_camp_img.set_colorkey(assets.key)


class LumberCamp(entity.Entity):
	def __init__(self, x, y, current_map):
        super().__init__()
        self.image = pygame.Surface([60, 60])
        self.image = lumber_camp_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.target = None

    def spawn_serf(self):
    	new_serf = serf.Serf(self.rect.x + 60, self.rect.y + 60, self.current_map)

  	def build(self, pos):
  		pygame.mouse.set_visible(0)
  		self.rect.x = pos[0]
  		self.rect.y = pos[1]

