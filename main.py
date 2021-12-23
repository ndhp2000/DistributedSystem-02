import pygame

from source.controller.controller import Controller, ServerIsOverload
from source.utils.log import GameLog
from source.view.menu import Menu

GameLog.load_config()

if __name__ == "__main__":
    pygame.init()
    pygame.mixer.init()
    menu = Menu()
    while True:
        player_choices = [0]
        menu.loop(player_choices)
        message = None

        try:
            controller = Controller(is_auto_play=player_choices[0] == 1)
            controller.loop()
            controller.close()
        except ConnectionAbortedError:
            message = "Can not connect to server"
        except ServerIsOverload:
            message = "Server is overload, try to play again later"

        menu.activate_menu(message)
