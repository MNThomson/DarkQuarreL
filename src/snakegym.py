import socket
import subprocess
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
        self.proc = subprocess.Popen(
            "battlesnake play --name Snake1 --url http://localhost:8080 --name Snake2 --url http://localhost:8000 -W 5 -H 5".split(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False,
        )

        self.observation = exampleMatrix()
        return self.observation

    def step(self, action):

        reward = 1
        done = False
        if action != 0:
            reward = 0
            done = True

        # self.isEnd()
        # state, reward, done, info = self._s.step(action)
        return self.observation, reward, done, None

    def isEnd(self):
        line = ""
        for line in self.proc.stderr:
            pass
        print(line)

    def render(self):
        raise NotImplementedError
        pprint(self.observation[1])

    def startHttpServer(self):
        SERVER_HOST = "127.0.0.1"
        SERVER_PORT = 8080

        # Create socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((SERVER_HOST, SERVER_PORT))
        self.server_socket.listen(1)
        print("Listening on port %s ..." % SERVER_PORT)
