import time

import numpy as np
import tensorflow as tf

import snakeGym
from dqn import Agent

if __name__ == "__main__":
    tf.compat.v1.disable_eager_execution()

    env = snakeGym.make("Battlegrounds-Duel")

    lr = 0.001
    n_games = 100000

    agent = Agent(
        gamma=0.99,
        epsilon=1.0,
        lr=lr,
        input_dims=env.observation_space.shape,
        n_actions=env.action_space,
        mem_size=1000000,
        batch_size=64,
        epsilon_end=0.01,
        fname="Battlegrounds-Duel.h5",
    )

    max_time = 18000
    start_time = time.time()  # remember when we started

    scores = []
    turns = []
    eps_history = []

    # agent.load_model()

    for section in range(1, (n_games // 100) + 1):
        section_scores = []
        section_turns = []
        section_eps_history = []
        for i in range(1, 101):
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
                # if i > n_games - 10:
                #     env.render()
                #     time.sleep(0.3)

                turn += 1

            section_eps_history.append(agent.epsilon)
            section_scores.append(score)
            section_turns.append(turn)

        avg_score = np.mean(section_scores)
        avg_turns = np.mean(section_turns)

        eps_history.append(agent.epsilon)
        scores.append(avg_score)
        turns.append(avg_turns)

        print(
            "episode: %5d" % (section * 100),
            "average_score: %5.2f" % avg_score,
            "epsilon: %.2f" % agent.epsilon,
            "average_turns: %5.2f" % avg_turns,
        )

        agent.save_model()

        if (time.time() - start_time) > max_time:
            break

    agent.save_model()

    x = [(i + 1) * 100 for i in range(len(scores))]
    env.plotLearning(x, scores, turns, "graph.png")
