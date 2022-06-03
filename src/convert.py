import json

import numpy as np


def snakeToArray(array, coords):
    array = coordinatesToArray(array, coords[1:])
    array[coords[0]["y"]][coords[0]["x"]] = 5
    return array


def coordinatesToArray(array, coords):
    for coord in coords:
        array[coord["y"]][coord["x"]] = 1
    return array


def convertJsonToMatrix(inputJson, depth):
    inputJson = json.loads(inputJson)
    board = inputJson["board"]
    snakes = board["snakes"]

    matrix = np.zeros(
        [depth, board["height"], board["width"]], dtype=np.int8
    )  # Create Matrix: 9 (Food + 8 snakes) x Height x Width

    matrix[0] = coordinatesToArray(matrix[0], board["food"])

    for i, snake in enumerate(snakes, 1):
        matrix[i] = snakeToArray(matrix[i], snake["body"])

    return matrix
