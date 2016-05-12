import pygame

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()

serf_grunt_1 = pygame.mixer.Sound("sound/serf/grunt1.wav")
serf_grunt_2 = pygame.mixer.Sound("sound/serf/grunt2.wav")
serf_grunt_3 = pygame.mixer.Sound("sound/serf/grunt3.wav")
serf_grunt_4 = pygame.mixer.Sound("sound/serf/grunt4.wav")


serf_grunts = [
    serf_grunt_1,
    serf_grunt_2,
    serf_grunt_3,
    serf_grunt_4
]
