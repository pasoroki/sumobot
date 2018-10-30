import pygame
from pygame.locals import QUIT, KEYDOWN, KEYUP
from threading import Event
import logging


LOG = logging.getLogger("joystick")


class Joystick:
    """
    Reads keyboard presses
    """
    _stop  = None
    _state = None

    def __init__(self, stop: Event, width: int=100, height: int=100):
        self._stop  = stop
        self._state = {}

        pygame.init()
        BLACK   = (0, 0, 0)
        self._width  = width
        self._height = height
        self._windowSurface = pygame.display.set_mode((width, height), 0, 32)
        self._windowSurface.fill(BLACK)

    @property
    def window(self):
        return self._windowSurface

    @property
    def get_buttons_state(self):
        """
        Get current state of pressed buttons
        """
        # state = {}
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                self._stop.set()

            if event.type == KEYDOWN:
                 key = event.key
                 self._state[key] = 1

            if event.type == KEYUP:
                 key = event.key
                 del(self._state[key])

        # return state
        # data = [str(key) for key in self._state.keys()]
        # print(" ".join(data))
        return self._state

    @property
    def state(self):
        print(" ".join(self._state))
        return self._state