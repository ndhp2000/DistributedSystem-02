import logging

from source.controller.controller import Controller
from source.utils.log import GameLog

GameLog.load_config()

if __name__ == "__main__":
    logger = logging.getLogger("game-debug")
    logger.info("Hello-World")
    controller = Controller(is_auto_play=False)
    controller.loop()
