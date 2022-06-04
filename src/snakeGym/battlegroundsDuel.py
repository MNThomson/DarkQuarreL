import json
from multiprocessing import Queue

import numpy as np

from convert import convertJsonToMatrix

from .baseEnv import BaseEnv


class BattlegroundsDuel(BaseEnv):
    def __init__(self) -> None:
        self.observation_space = np.zeros((3, 11, 11), dtype=np.int8)
        self.depth, self.height, self.width = self.observation_space.shape
        self.action_space = 4
        self.battleSnakeProc = None
        self.server_socket = None
        self.incomingQueue = Queue()
        self.outgoingQueue = Queue()

    def reset(self):
        self.killBattleSnakeRunner()

        self.startBattleSnakeRunner(
            snakes={
                "Snake1": "http://localhost:8080",
                "Snake2": "http://localhost:8000",
            }
        )

        self.observation = convertJsonToMatrix(self.incomingQueue.get(), self.depth)
        return self.observation

    def step(self, action):
        action = self.actionToStr(action)
        self.outgoingQueue.put(action)

        reward = 0
        done = False

        if not self.isEnd():
            data = self.incomingQueue.get()
            if data == "END":
                data = json.loads(self.incomingQueue.get())
                if len(data["board"]["snakes"]) == 0:
                    iWon = False
                else:
                    iWon = data["board"]["snakes"][0]["name"] == "Snake1"
                done = True
                reward = 1 if iWon else -1

            else:
                self.observation = convertJsonToMatrix(data, self.depth)

        return self.observation, reward, done, None

    def isEnd(self):
        return self.battleSnakeProc.poll() is None
