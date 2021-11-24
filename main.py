import logging

from source.controller.controller import Controller

if __name__ == "__main__":
    logger = logging.getLogger("game-debug")
    logger.info("Hello-World")
    controller = Controller()
    controller.loop()
