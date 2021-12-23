import pygame


class GameSound:
    VOLUME_SCALE = 0.2

    pygame.mixer.init()
    shoot_sound = pygame.mixer.Sound('assets/sounds/shoot.wav')
    menu_music = pygame.mixer.Sound('assets/sounds/menu_music.wav')
    gameplay_music = pygame.mixer.Sound('assets/sounds/gameplay_music.mp3')

    shoot_sound.set_volume(VOLUME_SCALE)
    menu_music.set_volume(VOLUME_SCALE)
    gameplay_music.set_volume(VOLUME_SCALE)