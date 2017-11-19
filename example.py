from random import choice
from gomoku_env import GomokuEnv
from gameloop import Game


try:  # python3 compatibility
    input = raw_input
except NameError:
    pass


def player1_turn(state):
    return choice(state.available_turns())


def player1_human_turn(state):
    _ = input("Type your turn as x,y: ")
    x, y = _.split(",")
    x, y = int(x.strip()), int(y.strip())
    return x, y


def player2_turn(state):
    return choice(state.available_turns())


env = GomokuEnv(board_size=15, win_len=5)
game = Game(env, player1_turn, player2_turn)
game.loop()
