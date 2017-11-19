from gomoku_env import BoardState


class Game(object):
    def __init__(self, env, agent1_func, agent2_func):
        self.env = env
        self.a1 = agent1_func
        self.a2 = agent2_func

    def loop(self):
        state = self.env.getstate()

        while True:
            p1_turn = self.a1(state)
            state, winner = self.env.step(BoardState.X, p1_turn)
            print(state.render())

            if winner != BoardState.NOBODY:
                if winner == BoardState.X:
                    print("---=== Winner: `X` ===---")
                elif winner == BoardState.O:
                    print("---=== Winner: `O` ===---")
                elif winner == BoardState.DRAW:
                    print("---=== Winner: `DRAW` ===---")
                return winner

            p2_turn = self.a2(state)
            state, winner = self.env.step(BoardState.O, p2_turn)
            print(state.render())

            if winner != BoardState.NOBODY:
                if winner == BoardState.X:
                    print("---=== Winner: `X` ===---")
                elif winner == BoardState.O:
                    print("---=== Winner: `O` ===---")
                elif winner == BoardState.DRAW:
                    print("---=== Winner: `DRAW` ===---")
                return winner
