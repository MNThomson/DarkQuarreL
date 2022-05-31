import socket
from pprint import pprint

import numpy as np

from convert import exampleMatrix


def make(str):
    return SoloArena()


class SoloArena:
    def __init__(self) -> None:
        self.observation_space = np.zeros((9, 11, 11), dtype=np.int8)
        self.action_space = 4
        self.observation = None
        self.proc = None

    def reset(self):
        self.observation = exampleMatrix()
        return self.observation

    def step(self, action):

        reward = 1
        done = False
        if action != 0:
            reward = 0
            done = True

        return self.observation, reward, done, None

    def render(self):
        pprint(self.observation[1])
