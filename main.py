import logging
import sys

from source.controller.controller import Controller, ServerIsOverload
from source.utils.log import GameLog

GameLog.load_config()

if __name__ == "__main__":
    logger = logging.getLogger("game-debug")
    logger.info("Hello-World")

    try:
        controller = Controller(is_auto_play=sys.argv[1] == "1", log_file_debug=sys.argv[2] + ".txt")
        # controller.menu()
        controller.loop()
    except ConnectionAbortedError:
        print("Can not connect to server")
    except ServerIsOverload:
        print("Server is overload, try to play again later")
