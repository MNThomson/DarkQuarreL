import tensorflow as tf

from convert import convertJsonToMatrix
from dqn import Agent


def get_info() -> dict:
    return {
        "apiversion": "1",
        "author": "MNThomson",
        "color": "#003049",
        "head": "evil",
        "tail": "hook",
    }


agent = None


def init():
    # tf.compat.v1.disable_eager_execution()
    global agent
    agent = Agent(
        gamma=0.99,
        epsilon=0.0,
        lr=0.01,
        input_dims=(3, 11, 11),
        n_actions=4,
        mem_size=1000000,
        batch_size=64,
        epsilon_end=0.0,
        fname="Battlegrounds-Duel.h5",
    )

    agent.load_model()


init()


def choose_move(data: dict) -> str:
    observation = convertJsonToMatrix(data, 3)

    global agent

    action = agent.choose_action(observation)

    move = ["up", "down", "left", "right"][action]

    return move
