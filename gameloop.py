class Game(object):
    def __init__(self, env, agent1_func, agent2_func):
        self.env = env
        self.a1 = agent1_func
        self.a2 = agent2_func

    def loop(self):
        while True:
            p1_turn = self.a1(self.env)
            winner = self.env.step(self.env.X, p1_turn)
            self.env.render()

            if winner != self.env.NOBODY:
                if winner == self.env.X:
                    print("---=== Winner: `X` ===---")
                elif winner == self.env.O:
                    print("---=== Winner: `O` ===---")
                elif winner == self.env.DRAW:
                    print("---=== Winner: `DRAW` ===---")
                return winner

            p2_turn = self.a2(self.env)
            winner = self.env.step(self.env.O, p2_turn)
            self.env.render()

            if winner != self.env.NOBODY:
                if winner == self.env.X:
                    print("---=== Winner: `X` ===---")
                elif winner == self.env.O:
                    print("---=== Winner: `O` ===---")
                elif winner == self.env.DRAW:
                    print("---=== Winner: `DRAW` ===---")
                return winner
