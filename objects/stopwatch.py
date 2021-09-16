from pygame import time

class Stopwatch():
    """The timer used in the game"""
    def __init__(self):
        self.t0 = time.get_ticks()

    def time_elapsed(self):
        return time.get_ticks() - self.t0

    def reset(self):
        self.t0 = time.get_ticks()