import pygame
from pygame.constants import *

from source.utils.assets import MenuViewAsset
from source.config import *
from source.utils.sound import GameSound
from source.view.button import Button
from source.view.input_box import InputBox
from source.view.spritesheet import SpriteSheet
from source.view.error import Error


class Menu:
    INPUT_BOX_OFFSET = (WIN_WIDTH / 2, 4 / 5 * WIN_HEIGHT)
    LOGO_OFFSET = (WIN_WIDTH / 2, 3 / 12 * WIN_HEIGHT)
    AUTOPLAY_BUTTON_OFFSET = (WIN_WIDTH / 2,  6 / 12 * WIN_HEIGHT)
    PLAY_BUTTON_OFFSET = (WIN_WIDTH / 2, 8 / 12 * WIN_HEIGHT)
    EXIT_BUTTON_OFFSET = (WIN_WIDTH / 2, 10 / 12 * WIN_HEIGHT)
    ERROR_MESSAGE_OFFSET = (WIN_WIDTH / 2, 1 / 12 * WIN_HEIGHT)

    INPUT_BOX_DIM = (30, 70)
    PLAY_BUTTON_DIM = (WIN_WIDTH / 3, WIN_HEIGHT / 8)
    AUTOPLAY_BUTTON_DIM = (WIN_WIDTH / 3, WIN_HEIGHT / 8)
    EXIT_BUTTON_DIM = (WIN_WIDTH / 3, WIN_HEIGHT / 8)

    BACKGROUND_RATIO = 160 / WIN_HEIGHT
    LOGO_SCALE_RATIO = 1.5

    def __init__(self):
        super().__init__()

        self._screen_display_ = pygame.display
        self._screen_display_.set_caption('Zace Maze')
        self._screen_ = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT), 0, 32)

        self._logo = pygame.image.load(MenuViewAsset.logo).convert_alpha()
        self._logo = pygame.transform.scale(self._logo,
                                            (self._logo.get_width() * self.LOGO_SCALE_RATIO,
                                             self._logo.get_height() * self.LOGO_SCALE_RATIO))
        self._input_box = InputBox(self.INPUT_BOX_OFFSET, self.INPUT_BOX_DIM)
        self._play_button = Button(self.PLAY_BUTTON_DIM, 'PLAY')
        self._auto_play_button = Button(self.AUTOPLAY_BUTTON_DIM, 'AUTOPLAY')
        self._exit_button = Button(self.EXIT_BUTTON_DIM, 'EXIT')
        self._background = SpriteSheet.image_at((0, 0), (WIN_WIDTH * self.BACKGROUND_RATIO, 160), 'MENU_BACKGROUND')

        self._is_click_input_box = False
        self._background = pygame.transform.scale(self._background, (WIN_WIDTH, WIN_HEIGHT))

        self._menu_active = True
        self._error_message = None

    def _add_child(self, surface, location):
        self._screen_.blit(surface, location)

    def _deactive_menu(self):
        self._menu_active = False

    def draw(self):
        self._add_child(self._background, self._background.get_rect(center=(WIN_WIDTH / 2, WIN_HEIGHT / 2)))
        self._add_child(self._logo, self._logo.get_rect(center=self.LOGO_OFFSET))
        self._play_button.add_to_parent(self._screen_, self.PLAY_BUTTON_OFFSET)
        self._auto_play_button.add_to_parent(self._screen_, self.AUTOPLAY_BUTTON_OFFSET)
        self._exit_button.add_to_parent(self._screen_, self.EXIT_BUTTON_OFFSET)

        if self._error_message is not None:
            self._error_message.add_to_parent(self._screen_, self.ERROR_MESSAGE_OFFSET)

        self._screen_display_.update()

    def handle_event(self, event, player_choices=None):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self._input_box.get_rect().collidepoint(event.pos):
                # Toggle the active variable.
                if self._input_box.is_active():
                    self._input_box.set_active(False)
                else:
                    self._input_box.set_active(True)
            elif self._play_button.get_rect(center=self.PLAY_BUTTON_OFFSET).collidepoint(event.pos):
                self._deactive_menu()
                player_choices[0] = MANUAL_PLAY
            elif self._auto_play_button.get_rect(center=self.AUTOPLAY_BUTTON_OFFSET).collidepoint(event.pos):
                self._deactive_menu()
                player_choices[0] = AUTO_PLAY
            elif self._exit_button.get_rect(center=self.EXIT_BUTTON_OFFSET).collidepoint(event.pos):
                pygame.quit()
                exit()

        if event.type == pygame.KEYDOWN:
            if self._input_box.is_active():
                if event.key == pygame.K_RETURN:
                    self._text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self._text = self._text[:-1]
                else:
                    self._text += event.unicode
                # Re-render the text.
                self._txt_surface = self._font.render(self._text, True, self._color)

    def click_input_box(self):
        self._is_click_input_box = ~self._is_click_input_box

    def get_input_name(self, event):
        self._input_box.handle_event(event)

    def is_active(self):
        return self._menu_active

    def activate_menu(self, error_message):
        self._menu_active = True
        self._error_message = Error(error_message)

    def loop(self, player_choices=None):
        GameSound.menu_music.play(-1)
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                    self.handle_event(event, player_choices)

            self.draw()

            if not self.is_active():
                GameSound.menu_music.stop()
                break