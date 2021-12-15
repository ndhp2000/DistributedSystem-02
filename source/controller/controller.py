import random
from queue import Queue
from sys import exit

import pygame
from pygame.locals import *

from source.config import *
from ..model.model import MainGameLogic
from ..network.network import GameNetwork
from ..view.view import MainGameView
from collections import deque


class Controller:
    COOLDOWN_COMMAND = 30

    def __init__(self, is_auto_play=False):
        self._is_bot_player = is_auto_play
        self._counter = self.COOLDOWN_COMMAND
        self._events_queue_ = deque()

        # Init Network
        self._network = GameNetwork()
        self._instance_id_, self._user_id_ = self._network.join_game()  # Sign-in to server.

        # Init state
        self._time_elapsed_ = 0
        self._current_frame_ = 0
        self._reset_state_()

    def _reset_state_(self):
        self._events_queue_.clear()
        # Get state form server
        initial_state = self._network.get_game_state(self._instance_id_, self._user_id_)
        self._current_frame_ = initial_state['current_frame']
        self._time_elapsed_ = initial_state['time_elapsed']
        self._clock = pygame.time.Clock()
        # Init Logic
        self._logic_ = MainGameLogic(initial_state['state']['seed'])
        self._logic_.init_maze(initial_state['state']['maze']['seed'])
        self._logic_.init_players(initial_state['state']['players'])
        self._logic_.init_bullets(initial_state['state']['bullets'])
        for event in initial_state['unprocessed_events']:
            self._events_queue_.append(event)
        # Init View
        self._view_ = MainGameView()
        self._view_.init_maze(self._logic_.get_maze())
        self._view_.init_scoreboard(self._logic_.get_players())
        self._view_.init_notification()
        self._view_.init_players(self._logic_.get_players())
        self._view_.init_bullets(self._logic_.get_bullets())
        self._view_.update()

    @staticmethod
    def _get_event_(key_pressed):
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

    def _event_generator_(self):  # Not used now
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

    def _enqueue_valid_events_(self, events):
        """
        :param events:
        :return: check if event is time-out
        """
        for event in events:
            if event['timeout'] < self._current_frame_:
                return False
            else:
                self._events_queue_.append(event)
        return True

    def _update(self):
        # Catch key event
        input_event = None
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if not self._is_bot_player:
                    input_event = self._get_event_(event.key)
        if self._is_bot_player:
            input_event = self._event_generator_()

        # Broadcast action
        if input_event:
            self._network.send_action(self._instance_id_, self._user_id_, input_event)

        # Get events from server to update
        events = self._network.receive(PROCESSED_EVENTS_PER_LOOPS)

        # Check if events is out of date and add to queue
        if not self._enqueue_valid_events_(events):
            self._reset_state_()
            return

        # Chose events to process in current frame
        processing_events = []
        while len(self._events_queue_):
            if self._events_queue_[0]['timeout'] == self._current_frame_:
                processing_events.append(self._events_queue_.popleft())
            else:
                break

        if len(processing_events):
            print("TIMER = ", self._time_elapsed_)
            print("EVENT_QUEUE = ", self._events_queue_)
            print("PROCESSING EVENTS = ", processing_events)

        # Update with events
        self._logic_.update(processing_events)
        self._view_.update()

    def loop(self):
        while True:
            while True:
                dt = self._clock.tick(30)
                self._time_elapsed_ += dt
                while self._time_elapsed_ >= FRAME_RATE_MS:
                    self._time_elapsed_ -= FRAME_RATE_MS
                    self._current_frame_ += 1
                    self._update()

# class Controller:
#     COOLDOWN_COMMAND = 30
#
#     def __init__(self, is_auto_play=False):
#         self._clock = pygame.time.Clock()
#         self._is_bot_player = is_auto_play
#         self._counter = self.COOLDOWN_COMMAND
#
#         # Init Logic
#         self._logic_ = MainGameLogic()
#         self._logic_.init_maze(1)
#         self._logic_.init_players()
#         self._logic_.init_bullets()
#
#         # Init View
#         self._view_ = MainGameView()
#         self._view_.init_maze(self._logic_.get_maze())
#         self._view_.init_scoreboard(self._logic_.get_players())
#         self._view_.init_notification()
#         self._view_.init_players(self._logic_.get_players())
#         self._view_.init_bullets(self._logic_.get_bullets())
#
#         # Init Network
#         # self._network = GameNetwork()
#
#     @staticmethod
#     def get_event(key_pressed):
#         if key_pressed == pygame.K_UP:
#             return UP
#         if key_pressed == pygame.K_DOWN:
#             return DOWN
#         if key_pressed == pygame.K_LEFT:
#             return LEFT
#         if key_pressed == pygame.K_RIGHT:
#             return RIGHT
#         if key_pressed == pygame.K_SPACE:
#             return SHOOT
#         return None
#
#     def _event_generator(self):  # Not used now
#         """
#         Create random event for bot player
#         :return: event
#         """
#         self._counter -= 1
#         if self._counter == 0:
#             self._counter = self.COOLDOWN_COMMAND
#             rand_num = random.randint(-N_TYPE_COMMANDS, N_TYPE_COMMANDS - 1)  # TODO UPDATE FOR BACKEND
#             if rand_num < 0:
#                 return SHOOT
#             else:
#                 return list(PLAYER_MOVEMENT.keys())[rand_num - 1]
#         return None
#
#     def loop(self):
#         while True:
#             dt = self._clock.tick(60) / 1000
#             input_event = None
#
#             for event in pygame.event.get():
#                 if event.type == QUIT:
#                     pygame.quit()
#                     exit()
#                 if event.type == pygame.KEYDOWN:
#                     if not self._is_bot_player:
#                         input_event = self.get_event(event.key)
#                         print(input_event)
#
#             if self._is_bot_player:
#                 input_event = self._event_generator()
#             # TODO: Send packet to server
#
#             # events = self._network.receive(PROCESSED_EVENTS_PER_LOOPS)
#             # self._logic_.update(events, dt)
#
#             self._logic_.update(input_event, dt)
#
#             self._view_.update()
