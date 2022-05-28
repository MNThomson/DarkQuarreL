import random
from turtle import pos
from typing import List, Dict

"""
This file can be a nice home for your Battlesnake's logic and helper functions.

We have started this for you, and included some logic to remove your Battlesnake's 'neck'
from the list of possible moves!
"""
def get_info() -> dict:
    """
    This controls your Battlesnake appearance and author permissions.
    For customization options, see https://docs.battlesnake.com/references/personalization

    TIP: If you open your Battlesnake URL in browser you should see this data.
    """
    return {
        "apiversion": "1",
        "author": "Snattle",
        "color": "#888888",
        "head": "caffeine",
        "tail": "bolt",
    }


def choose_move(data: dict) -> str:
    """
    data: Dictionary of all Game Board data as received from the Battlesnake Engine.
    For a full example of 'data', see https://docs.battlesnake.com/references/api/sample-move-request

    return: A String, the single move to make. One of "up", "down", "left" or "right".

    Use the information in 'data' to decide your next move. The 'data' variable can be interacted
    with as a Python Dictionary, and contains all of the information about the Battlesnake board
    for each move of the game.

    """
    my_snake = data["you"]      # A dictionary describing your snake's position on the board
    my_head = my_snake["head"]  # A dictionary of coordinates like {"x": 0, "y": 0}
    my_body = my_snake["body"]  # A list of coordinate dictionaries like [{"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0}]

    # Uncomment the lines below to see what this data looks like in your output!
    # print(f"~~~ Turn: {data['turn']}  Game Mode: {data['game']['ruleset']['name']} ~~~")
    # print(f"All board data this turn: {data}")
    # print(f"My Battlesnake this turn is: {my_snake}")
    print(f"My Battlesnakes head this turn is: {my_head}")
    # print(f"My Battlesnakes body this turn is: {my_body}")

    possible_moves = ["up", "down", "left", "right"]

    # Step 0: Don't allow your Battlesnake to move back on it's own neck.
    possible_moves = avoid_neck(possible_moves, my_body)

    # TODO: Step 1 - Don't hit walls.
    # Use information from `data` and `my_head` to not move beyond the game board.
    board = data['board']
    board_height = board['height']
    board_width = board['width']
    # print(board_height, board_width)

    possible_moves = avoid_walls(possible_moves, my_head, board_height, board_width)

    # TODO: Step 2 - Don't hit yourself.
    # Use information from `my_body` to avoid moves that would collide with yourself.
    possible_moves = avoid_body(possible_moves, my_body)

    # TODO: Step 3 - Don't collide with others.
    # Use information from `data` to prevent your Battlesnake from colliding with others.

    possible_moves = avoid_other_snakes(possible_moves, my_head, board["snakes"])
    # TODO: Step 4 - Find food.
    # Use information in `data` to seek out and find food.
    # food = data['board']['food']

    # Choose a random direction from the remaining possible_moves to move in, and then return that move
    if not possible_moves:
        print("NO POSSIBLE MOVES")
        return "up"
    move = random.choice(possible_moves)
    # TODO: Explore new strategies for picking a move that are better than random

    print(f"{data['game']['id']} MOVE {data['turn']}: {move} picked from all valid options in {possible_moves}")

    return move


def avoid_neck(possible_moves: List[str], my_body: dict) -> List[str]:
    """
    my_body: List of dictionaries of x/y coordinates for every segment of a Battlesnake.
            e.g. [{"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0}]
    possible_moves: List of strings. Moves to pick from.
            e.g. ["up", "down", "left", "right"]

    return: The list of remaining possible_moves, with the 'neck' direction removed
    """
    my_head = my_body[0]  # The first body coordinate is always the head
    my_neck = my_body[1]  # The segment of body right after the head is the 'neck'

    if my_neck["x"] < my_head["x"]:  # my neck is left of my head
        possible_moves.remove("left")
    elif my_neck["x"] > my_head["x"]:  # my neck is right of my head
        possible_moves.remove("right")
    elif my_neck["y"] < my_head["y"]:  # my neck is below my head
        possible_moves.remove("down")
    elif my_neck["y"] > my_head["y"]:  # my neck is above my head
        possible_moves.remove("up")

    return possible_moves

def avoid_walls(possible_moves: List[str], head: List[str], height: int, width: int) -> List[str]:
    if head["x"] == 0:
        possible_moves.remove("left")
    elif head["x"] == width - 1:
        possible_moves.remove("right")
    if head["y"] == 0:
        possible_moves.remove("down")
    elif head["y"] == height - 1:
        possible_moves.remove("up")

    return possible_moves

def avoid_body(possible_moves: List[str], body: List[str]) -> List[str]:
    if {"x": body[0]["x"] - 1, "y": body[0]["y"]} in body:
        if "left" in possible_moves: possible_moves.remove("left")
    if {"x": body[0]["x"] + 1, "y": body[0]["y"]} in body:
        if "right" in possible_moves: possible_moves.remove("right")
    if {"x": body[0]["x"], "y": body[0]["y"] - 1} in body:
        if "down" in possible_moves: possible_moves.remove("down")
    if {"x": body[0]["x"], "y": body[0]["y"] + 1} in body:
        if "up" in possible_moves: possible_moves.remove("up")

    return possible_moves

def avoid_other_snakes(possible_moves: List[str], head, other_snakes: List[str]) -> List[str]:
    for snake in other_snakes:
        if {"x": head["x"] - 1, "y": head["y"]} in snake["body"]:
            if "left" in possible_moves: possible_moves.remove("left")
        if {"x": head["x"] + 1, "y": head["y"]} in snake["body"]:
            if "right" in possible_moves: possible_moves.remove("right")
        if {"x": head["x"], "y": head["y"] - 1} in snake["body"]:
            if "down" in possible_moves: possible_moves.remove("down")
        if {"x": head["x"], "y": head["y"] + 1} in snake["body"]:
            if "up" in possible_moves: possible_moves.remove("up")

    return possible_moves
