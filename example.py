from random import choice
from gomoku_env import GomokuEnv


def player1_turn(env):
    return choice(env.available_turns())


def player2_turn(env):
    return choice(env.available_turns())


env = GomokuEnv(board_size=3, win_len=3)

while True:
    p1_turn = player1_turn(env)
    winner = env.step(env.X, p1_turn)
    env.render()

    if winner != env.NOBODY:
        if winner == env.X:
            print("---=== Winner: `X` ===---")
        elif winner == env.O:
            print("---=== Winner: `O` ===---")
        elif winner == env.DRAW:
            print("---=== Winner: `DRAW` ===---")
        break

    p2_turn = player2_turn(env)
    winner = env.step(env.O, p2_turn)
    env.render()

    if winner != env.NOBODY:
        if winner == env.X:
            print("---=== Winner: `X` ===---")
        elif winner == env.O:
            print("---=== Winner: `O` ===---")
        elif winner == env.DRAW:
            print("---=== Winner: `DRAW` ===---")
        break
