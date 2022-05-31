import time
from pprint import pprint

import numpy as np
import tensorflow as tf

import snakegym
from dqn import Agent
from utils import plotLearning

if __name__ == "__main__":
    tf.compat.v1.disable_eager_execution()

    env = snakegym.make("Solo-Arena")

    lr = 0.001
    n_games = 500

    agent = Agent(
        gamma=0.99,
        epsilon=1.0,
        lr=lr,
        input_dims=env.observation_space.shape,
        n_actions=env.action_space,
        mem_size=1000000,
        batch_size=64,
        epsilon_end=0.01,
    )

    scores = []
    eps_history = []
    # agent.load_model()
    for i in range(n_games):
        starttime = time.time()

        done = False
        score = 0
        observation = env.reset()
        while not done:
            action = agent.choose_action(observation)
            observation_, reward, done, info = env.step(action)
            score += reward
            agent.store_transition(observation, action, reward, observation_, done)
            observation = observation_
            agent.learn()

        totaltime = time.time() - starttime

        eps_history.append(agent.epsilon)
        scores.append(score)

        avg_score = np.mean(scores[-100:])
        print(
            "episode:",
            i,
            "score %.2f" % score,
            "average_score %.2f" % avg_score,
            "epsilon %.2f" % agent.epsilon,
            "time %.2f" % totaltime,
        )

    # agent.save_model()

    filename = "graph.png"
    x = [i + 1 for i in range(n_games)]
    plotLearning(x, scores, eps_history, filename)
