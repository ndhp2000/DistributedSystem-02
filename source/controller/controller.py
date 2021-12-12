import random
from sys import exit

import pygame
from pygame.locals import *

from source.config import *
from ..model.model import MainGameLogic
from ..network.network import GameNetwork
from ..view.view import MainGameView


class Controller:
    COOLDOWN_COMMAND = 30

    def __init__(self, is_auto_play=False):
        self._clock = pygame.time.Clock()
        self._is_bot_player = is_auto_play
        self._counter = self.COOLDOWN_COMMAND

        # Init Logic
        self._logic_ = MainGameLogic()
        self._logic_.init_maze()
        self._logic_.init_players()
        self._logic_.init_bullets()

        # Init View
        self._view_ = MainGameView()
        self._view_.init_maze(self._logic_.get_maze())
        self._view_.init_scoreboard(self._logic_.get_players())
        self._view_.init_notification()
        self._view_.init_players(self._logic_.get_players())
        self._view_.init_bullets(self._logic_.get_bullets())

        # Init Network
        # self._network = GameNetwork()

    @staticmethod
    def get_event(key_pressed):
        if key_pressed == pygame.K_UP:
            return UP
        if key_pressed == pygame.K_DOWN:
            return DOWN
        if key_pressed == pygame.K_LEFT:
            return LEFT
        if key_pressed == pygame.K_RIGHT:
            return RIGHT
        if key_pressed == pygame.K_SPACE:
            return SHOOT
        return None

    def _event_generator(self):  # Not used now
        """
        Create random event for bot player
        :return: event
        """
        self._counter -= 1
        if self._counter == 0:
            self._counter = self.COOLDOWN_COMMAND
            rand_num = random.randint(-N_TYPE_COMMANDS, N_TYPE_COMMANDS - 1)  # TODO UPDATE FOR BACKEND
            if rand_num < 0:
                return SHOOT
            else:
                return list(PLAYER_MOVEMENT.keys())[rand_num - 1]
        return None

    def loop(self):
        while True:
            dt = self._clock.tick(60) / 1000

            input_event = None
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if self._is_bot_player:
                        input_event = self._event_generator()
                    else:
                        input_event = self.get_event(event.key)
                # TODO: Send packet to server

            # events = self._network.receive(PROCESSED_EVENTS_PER_LOOPS)
            # self._logic_.update(events, dt)

            self._logic_.update(input_event, dt)

            self._view_.update()
