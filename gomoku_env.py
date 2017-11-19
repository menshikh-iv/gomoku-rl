import numpy as np


class GomokuEnv(object):
    NOBODY = 0
    X = 1
    O = 2
    DRAW = 3

    def __init__(self, board_size=19, win_len=5):
        assert board_size >= 3
        assert win_len >= 3

        self._field = None
        self._current_step = GomokuEnv.X
        self._size = board_size
        self._win_len = win_len
        self.reset()

    def reset(self):
        self._field = np.zeros((self._size, self._size), dtype=int)

    def step(self, player, action):
        if player not in {GomokuEnv.X, GomokuEnv.O}:
            raise ValueError("Incorrect player {} (must be {} or {})".format(player, GomokuEnv.X, GomokuEnv.O))

        if player != self._current_step:
            raise ValueError("Incorrect player {}, now it's {} turn".format(player, self._current_step))

        x, y = action
        if x >= self._size or y >= self._size or x < 0 or y < 0:
            raise ValueError("Action {} out of field ({} X {})".format(action, self._size, self._size))

        if self._field[x][y] != 0:
            raise RuntimeError("Incorrect move {}, this cell already filled".format(action))

        self._field[x][y] = player
        self._current_step = GomokuEnv.X if player == GomokuEnv.O else GomokuEnv.O
        return np.copy(self._field), self._who_is_winner()

    def _who_is_winner(self):
        combinations = \
            [self._field[::-1, :].diagonal(i).tolist()
             for i in range(-self._field.shape[0] + 1, self._field .shape[1])] + \
            [self._field.diagonal(i).tolist()
             for i in range(self._field.shape[1] - 1, -self._field.shape[0], -1)] + \
            [self._field[idx][a: b].tolist()
             for a in range(self._size)
             for b in range(self._size)
             for idx in range(self._size)
             if (b - a) == self._win_len] + \
            [self._field[::-1, :][idx][a: b].tolist()
             for a in range(self._size)
             for b in range(self._size)
             for idx in range(self._size)
             if (b - a) == self._win_len]

        combinations = [set(_) for _ in combinations if len(_) >= self._win_len]

        if {GomokuEnv.O} in combinations:
            return GomokuEnv.O

        if {GomokuEnv.X} in combinations:
            return GomokuEnv.X

        if np.count_nonzero(self._field) == self._size * self._size:
            return GomokuEnv.DRAW

        return GomokuEnv.NOBODY

    def render(self):
        result_str = "Next turn - `{}`\n".format("X" if self._current_step == GomokuEnv.X else "O")
        result_str += "-\t" * (self._size + 2) + "\n"
        for row in self._field:
            result_str += "|\t"
            for el in row:
                if el == GomokuEnv.NOBODY:
                    result_str += ".\t"
                    continue
                result_str += "X\t" if el == GomokuEnv.X else "O\t"
            result_str += "|\n"
        result_str += "-\t" * (self._size + 2) + "\n"
        return result_str
