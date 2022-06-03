import numpy as np

from .utils import plotLearning


class BaseEnv:
    def plotLearning(self, x, scores, epsilons, filename, lines=None):
        plotLearning(x, scores, epsilons, filename, lines)

    def render(self):
        print("New Board State")
        boardToPrint = np.full((11, 11), "░░", dtype=object)
        snakeIcons = ["⬜", "🟨", "🟥", "🟪", "🟩", "🟧", "🟫", "🟦"]

        for yLevel, y in enumerate(self.observation[0]):
            for xLevel, x in enumerate(y):
                if x != 0:
                    boardToPrint[yLevel][xLevel] = "🍎"

        for snakeNumber, state in enumerate(self.observation[1:]):
            for yLevel, y in enumerate(state):
                for xLevel, x in enumerate(y):
                    if x != 0:
                        boardToPrint[yLevel][xLevel] = snakeIcons[snakeNumber]

        for i in boardToPrint:
            for j in i:
                print(j, end="")
            print()
