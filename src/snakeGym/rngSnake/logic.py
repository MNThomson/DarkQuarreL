import random


def get_info() -> dict:
    return {
        "apiversion": "1",
        "author": "rngSnake",
        "color": "#ff0000",
        "head": "default",
        "tail": "default",
    }


def choose_move(data: dict) -> str:
    my_snake = data["you"]
    my_head = my_snake["head"]
    my_body = my_snake["body"]

    possible_moves = ["up", "down", "left", "right"]

    board = data["board"]
    board_height = board["height"]
    board_width = board["width"]

    possible_moves = avoid_walls(possible_moves, my_head, board_height, board_width)

    # Don't hit itself.
    possible_moves = avoid_body(possible_moves, my_body)

    # Don't collide with others.
    possible_moves = avoid_other_snakes(possible_moves, my_head, board["snakes"])

    # Choose a random direction from the remaining possible_moves to move in, and then return that move
    if not possible_moves:
        return possible_moves.append("up")
    move = random.choice(possible_moves)

    return move


def avoid_walls(possible_moves, head, height: int, width: int):
    if head["x"] == 0:
        possible_moves.remove("left")
    elif head["x"] == width - 1:
        possible_moves.remove("right")
    if head["y"] == 0:
        possible_moves.remove("down")
    elif head["y"] == height - 1:
        possible_moves.remove("up")

    return possible_moves


def avoid_body(possible_moves, body):
    if {"x": body[0]["x"] - 1, "y": body[0]["y"]} in body:
        if "left" in possible_moves:
            possible_moves.remove("left")
    if {"x": body[0]["x"] + 1, "y": body[0]["y"]} in body:
        if "right" in possible_moves:
            possible_moves.remove("right")
    if {"x": body[0]["x"], "y": body[0]["y"] - 1} in body:
        if "down" in possible_moves:
            possible_moves.remove("down")
    if {"x": body[0]["x"], "y": body[0]["y"] + 1} in body:
        if "up" in possible_moves:
            possible_moves.remove("up")

    return possible_moves


def avoid_other_snakes(possible_moves, head, other_snakes):
    for snake in other_snakes:
        if {"x": head["x"] - 1, "y": head["y"]} in snake["body"]:
            if "left" in possible_moves:
                possible_moves.remove("left")
        if {"x": head["x"] + 1, "y": head["y"]} in snake["body"]:
            if "right" in possible_moves:
                possible_moves.remove("right")
        if {"x": head["x"], "y": head["y"] - 1} in snake["body"]:
            if "down" in possible_moves:
                possible_moves.remove("down")
        if {"x": head["x"], "y": head["y"] + 1} in snake["body"]:
            if "up" in possible_moves:
                possible_moves.remove("up")

    return possible_moves
