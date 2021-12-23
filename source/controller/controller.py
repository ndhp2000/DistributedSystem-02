import random
from collections import deque
from sys import exit

import pygame
from pygame.locals import *

from source.config import *
from ..model.model import MainGameLogic
from ..network.network import GameNetwork
from ..view.view import MainGameView


class ServerIsOverload(Exception):
    pass


class Controller:
    COOLDOWN_COMMAND = 5

    def __init__(self, is_auto_play=False, log_file_debug="a.txt"):
        # TODO - DELETE
        self.debug_file = open(log_file_debug, "w")

        self._exit_flag = False
        self._is_bot_player = is_auto_play
        self._counter = self.COOLDOWN_COMMAND
        self._events_queue_ = deque()

        # Init Network
        self._network = GameNetwork()
        self._instance_id_, self._user_id_ = self._network.join_game()  # Sign-in to server.
        if self._instance_id_ is None:
            self._network.safety_closed()
            raise ServerIsOverload

        # Init state
        self._time_elapsed_ = 0
        self._current_frame_ = 0
        self._reset_state_()

    def _reset_state_(self):
        self._events_queue_.clear()
        # Get state form server
        initial_state = self._network.get_game_state(self._instance_id_, self._user_id_)
        self._current_frame_ = initial_state['current_frame'] - 1
        self._time_elapsed_ = initial_state['time_elapsed'] + FRAME_RATE_MS
        self._clock = pygame.time.Clock()
        self._clock.tick()

        # Init Logic
        self._logic_ = MainGameLogic()
        self._logic_.init_maze(initial_state['state']['maze']['seed'])
        self._logic_.init_notification()
        self._logic_.init_players(initial_state['state']['players'], self._user_id_)
        self._logic_.init_bullets(initial_state['state']['bullets'])
        for event in initial_state['unprocessed_events']:
            self._events_queue_.append(event)
        # Init View
        self._view_ = MainGameView()
        self._view_.init_maze(self._logic_.get_maze())
        self._view_.init_scoreboard(self._logic_.get_players())
        self._view_.init_notification(self._logic_.get_notification())
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
        if key_pressed == pygame.K_q:
            return EXIT
        return None

    def _event_generator_(self):
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
        for event in events:
            if event['timeout'] < self._current_frame_:
                return False
            else:
                self._events_queue_.append(event)
        return True

    def _update(self, update_view=True):
        # Catch key event
        input_event = None
        if update_view:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    self.close()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if not self._is_bot_player:
                        input_event = self._get_event_(event.key)
                    if event.key == pygame.K_q:
                        self._exit_flag = True
            if self._is_bot_player:
                input_event = self._event_generator_()

        # Broadcast action
        if input_event:
            self._network.send_action(self._instance_id_, self._user_id_, input_event)

        # Get events from server to update
        events = self._network.receive(PROCESSED_EVENTS_PER_LOOPS)

        # Check if events is out of date and add to queue
        if not self._enqueue_valid_events_(events):
            self.debug_file.write("RESET\n")
            self._reset_state_()
            return

        # Chose events to process in current frame
        processing_events = []
        while len(self._events_queue_):
            if self._events_queue_[0]['timeout'] == self._current_frame_:
                processing_events.append(self._events_queue_.popleft())
            else:
                break

        # Update with events
        self._logic_.update(processing_events, self._user_id_)
        if update_view:
            self._view_.update()
        self.debug_file.write(str(self._current_frame_) + " : " + str(self._logic_.serialize()) + "\n")

    def loop(self):
        while not self._exit_flag:
            dt = self._clock.tick(FRAME_RATE)
            self._time_elapsed_ += dt
            while self._time_elapsed_ >= FRAME_RATE_MS:
                self._time_elapsed_ -= FRAME_RATE_MS
                self._current_frame_ += 1
                self._update(update_view=self._time_elapsed_ < FRAME_RATE_MS)

    def close(self):
        self.debug_file.close()
        self._network.safety_closed()
