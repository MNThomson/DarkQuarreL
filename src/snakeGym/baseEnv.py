from .utils import plotLearning


class BaseEnv:
    def plotLearning(self, x, scores, epsilons, filename, lines=None):
        plotLearning(x, scores, epsilons, filename, lines)
