import pygame
from source.config import *
from source.view.input_box import InputBox
from source.view.spritesheet import SpriteSheet


class Menu:
    INPUT_BOX_OFFSET = (WIN_WIDTH / 2, 4 / 5 * WIN_HEIGHT)
    AUTOPLAY_BUTTON_OFFSET = (WIN_WIDTH / 2,  2 / 8 * WIN_HEIGHT)
    PLAY_BUTTON_OFFSET = (WIN_WIDTH / 2, 4 / 8 * WIN_HEIGHT)
    EXIT_BUTTON_OFFSET = (WIN_WIDTH / 2, 6 / 8 * WIN_HEIGHT)

    INPUT_BOX_DIM = (30, 70)
    PLAY_BUTTON_DIM = (WIN_WIDTH / 3, WIN_HEIGHT / 5)
    EXIT_BUTTON_DIM = (WIN_WIDTH / 3, WIN_HEIGHT / 5)
    BACKGROUND_RATIO = 160 / WIN_HEIGHT

    def __init__(self):
        super().__init__()
        self._input_box = InputBox(self.INPUT_BOX_OFFSET, self.INPUT_BOX_DIM)
        self._play_button = SpriteSheet.image_at((0, 0), (600, 200), 'MENU')
        # self._auto_play_button = pygame
        # self._play_button =
        self._exit_button = SpriteSheet.image_at((1215, 625), (600, 200), 'MENU')
        self._background = SpriteSheet.image_at((0, 0), (WIN_WIDTH * self.BACKGROUND_RATIO, 160), 'MENU_BACKGROUND')

        self._is_click_input_box = False

        self._play_button = pygame.transform.scale(self._play_button, self.PLAY_BUTTON_DIM)
        self._exit_button = pygame.transform.scale(self._exit_button, self.EXIT_BUTTON_DIM)
        self._background = pygame.transform.scale(self._background, (WIN_WIDTH, WIN_HEIGHT))

        self._screen_display_ = pygame.display
        self._screen_display_.set_caption('Zace Maze')
        self._screen_ = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT), 0, 32)

        self._menu_active = True

    def _add_child(self, surface, location):
        self._screen_.blit(surface, location)

    def _deactive_menu(self):
        self._menu_active = False

    def draw(self):
        self._add_child(self._background, self._background.get_rect(center=(WIN_WIDTH / 2, WIN_HEIGHT / 2)))
        self._add_child(self._play_button, self._play_button.get_rect(center=self.PLAY_BUTTON_OFFSET))
        self._add_child(self._exit_button, self._exit_button.get_rect(center=self.EXIT_BUTTON_OFFSET))

        self._screen_display_.update()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self._input_box.get_rect().collidepoint(event.pos):
                print('test input')
                # Toggle the active variable.
                if self._input_box.is_active():
                    self._input_box.set_active(False)
                else:
                    self._input_box.set_active(True)
            elif self._play_button.get_rect(center=self.PLAY_BUTTON_OFFSET).collidepoint(event.pos):
                self._deactive_menu()
            elif self._exit_button.get_rect(center=self.EXIT_BUTTON_OFFSET).collidepoint(event.pos):
                pygame.quit()
                exit()

        if event.type == pygame.KEYDOWN:
            if self._input_box.is_active():
                if event.key == pygame.K_RETURN:
                    print(self._text)
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