import numpy as np

LOGGER = [("game-debug", "./logs"), ("game-view", "./logs"), ("game-controller", "./logs"),
          ("game-model", "./logs"),
          ("game-socket", "./logs")]
MAP_WIDTH = 32
MAP_HEIGHT = 16
WIN_WIDTH = 1024
WIN_HEIGHT = 768
NAME_TAG_FONT_SIZE = 32
CONSOLE_FONT_SIZE = 18

SERVER_IP = '127.0.0.1'
SERVER_PORT = 12345
PROCESSED_EVENTS_PER_LOOPS = 10

PLAYER = "human"
MACHINE = "machine"
ENEMY = "enemy"

PLAYER_HP = 10
PLAYER_MOVING_SPEED = 4
PLAYER_RADIUS = 7
PLAYER_MAZE_RADIUS = 0.5
PLAYER_REWARD = 11

COLLISION_RANGE = 0.25 # Maze distance

BULLET_MOVING_SPEED = 2 * PLAYER_MOVING_SPEED
BULLET_MAZE_RADIUS = 0.2
BULLET_RADIUS = 3
BULLET_DAMAGE = 5
BULLET_COST = 1
COOLDOWN_RANGE = 4

N_TYPE_COMMANDS = 5
UP = 1
DOWN = -1
LEFT = 2
RIGHT = -2
SHOOT = 3
EXIT = 4

DIRECTIONS = {
    UP: np.array([0, -1]),
    DOWN: np.array([0, 1]),
    LEFT: np.array([-1, 0]),
    RIGHT: np.array([1, 0])
}

EVENT_TYPE = {
    'PLAYER_MOVEMENT': 0,
    'PLAYER_SHOOT': 1
}

PLAYER_MOVEMENT = {
    UP: UP,
    DOWN: DOWN,
    LEFT: LEFT,
    RIGHT: RIGHT
}

PLAYER_SHOOT = {
    SHOOT: SHOOT
}

MAZE_SCREEN_RATIO = (2 / 3, 1)
DAMAGE = 5
