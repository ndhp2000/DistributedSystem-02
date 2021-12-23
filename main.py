import logging
import sys

import pygame

from source.controller.controller import Controller, ServerIsOverload, ExitToGameMenu
from source.utils.log import GameLog
from source.view.menu import Menu

GameLog.load_config()

if __name__ == "__main__":
    logger = logging.getLogger("game-debug")
    logger.info("Hello-World")

    pygame.init()
    pygame.mixer.init()
    menu = Menu()

    while True:
        menu.loop()

        try:
            controller = Controller(is_auto_play=sys.argv[1] == "1", log_file_debug=sys.argv[2] + ".txt")
            controller.loop()
            controller.close()
        except ConnectionAbortedError:
            #menu.print("Can not connect to server")
            print("Can not connect to server")
        except ServerIsOverload:
            #menu.print("Server is overload, try to play again later")
            print("Server is overload, try to play again later")

        menu.activate_menu()


