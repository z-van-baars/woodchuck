import pygame

black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
blue_grey = (180, 210, 217)
purple = (255, 0, 255)
gold = (255, 187, 0)
key = (255, 0, 128)


pygame.display.set_caption("woodchuck")
screen_width = 1920
screen_height = 1080
screen = pygame.display.set_mode([screen_width, screen_height])
green_background = pygame.image.load("art/grass_bg.png").convert()
