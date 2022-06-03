import time

import numpy as np
import tensorflow as tf

import snakeGym
from dqn import Agent

if __name__ == "__main__":
    tf.compat.v1.disable_eager_execution()

    env = snakeGym.make("Battlegrounds-Duel")

    lr = 0.001
    n_games = 1000

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
    turns = []
    eps_history = []
    # agent.load_model()
    for i in range(n_games):
        starttime = time.time()

        done = False
        score = 0
        turn = 0
        observation = env.reset()
        while not done:
            action = agent.choose_action(observation)
            observation_, reward, done, info = env.step(action)
            score += reward
            agent.store_transition(observation, action, reward, observation_, done)
            observation = observation_
            agent.learn()
            if i % 100 == 0 or i > n_games - 10:
                env.render()
                time.sleep(0.3)

            turn += 1

        totaltime = time.time() - starttime

        eps_history.append(agent.epsilon)
        scores.append(score)
        turns.append(turn)

        if i % 100 == 0 or score == 1:
            avg_score = np.mean(scores[-100:])
            avg_turns = np.mean(turns[-100:])
            print(
                "episode:",
                i,
                "score %.2f" % score,
                "average_score %.2f" % avg_score,
                "epsilon %.2f" % agent.epsilon,
                "time %.2f" % totaltime,
                "average_turns %.2f" % avg_turns,
            )

    # agent.save_model()

    x = [i + 1 for i in range(n_games)]
    env.plotLearning(x, scores, eps_history, "graph.png")
