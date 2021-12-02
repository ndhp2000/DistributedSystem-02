import numpy as np

LOGGER = [("game-debug", "./logs"), ("game-view", "./logs"), ("game-controller", "./logs"),
          ("game-modeimport numpy as np

LOGGER = [("game-debug", "./logs"), ("game-view", "./logs"), ("game-controller", "./logs"),
          ("game-model", "./logs"),
          ("game-socket", "./logs")]
MAP_WIDTH = 32
MAP_HEIGHT = 16
WIN_WIDTH = 1024
WIN_HEIGHT = 768

STOP = 0
UP = 1
DOWN = -1
LEFT = 2
RIGHT = -2
SHOOT = 3

DIRECTIONS = {
    STOP: np.array([0, 0]), 
    UP: np.array([0, -1]), 
    DOWN: np.array([0, 1]), 
    LEFT: np.array([-1, 0]), 
    RIGHT: np.array([1, 0])
}