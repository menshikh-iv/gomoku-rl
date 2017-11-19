from random import choice
from gomoku_env import GomokuEnv


def player1_turn(available_turns):
    return choice(available_turns)


def player2_turn(available_turns):
    return choice(available_turns)


env = GomokuEnv(board_size=3, win_len=3)

while True:
    print("step")
    environment, winner = env.step(env.X, player1_turn(env.available_turns()))
    print(env.render())

    if winner != env.NOBODY:
        if winner == env.X:
            print("---=== Winner: `X` ===---")
        elif winner == env.O:
            print("---=== Winner: `O` ===---")
        elif winner == env.DRAW:
            print("---=== Winner: `DRAW` ===---")
        break

    environment, winner = env.step(env.O, player2_turn(env.available_turns()))
    print(env.render())

    if winner != env.NOBODY:
        if winner == env.X:
            print("---=== Winner: `X` ===---")
        elif winner == env.O:
            print("---=== Winner: `O` ===---")
        elif winner == env.DRAW:
            print("---=== Winner: `DRAW` ===---")
        break
