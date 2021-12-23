import pygame


class GameSound:
    pygame.mixer.init()
    shoot_sound = pygame.mixer.Sound('assets/sounds/shoot.wav')
    menu_music = pygame.mixer.Sound('assets/sounds/menu_music.wav')
    gameplay_music = pygame.mixer.Sound('assets/sounds/gameplay_music.mp3')