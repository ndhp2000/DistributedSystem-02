# Register Logger
import logging

from source.utils.log import GameLog

if __name__ == "__main__":
    GameLog.load_config()
    logger = logging.getLogger("game-debug")
    logger.info("Hello-World")
    # TODO: write new things here
