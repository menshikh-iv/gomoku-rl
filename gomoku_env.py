import itertools as it
import numpy as np


class GomokuEnv(object):
    NOBODY = 0
    X = 1
    O = 2
    DRAW = 3

    @staticmethod
    def get_all_diags(matr):
        return \
            [matr[::-1, :].diagonal(i).tolist() for i in range(-matr.shape[0] + 1, matr.shape[1])] + \
            [matr.diagonal(i).tolist() for i in range(matr.shape[1] - 1, -matr.shape[0], -1)]

    @staticmethod
    def comb(arr, size):
        if len(arr) == 3:
            return [arr]

        return [arr[a: b] for a, b in zip(range(0, len(arr) - size + 1), range(size, len(arr) + 1))]

    def __init__(self, board_size, win_len):
        assert board_size >= 3
        assert win_len >= 3
        assert win_len <= board_size

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
        return self._who_is_winner()

    def _who_is_winner(self):
        combinations = GomokuEnv.get_all_diags(self._field)
        combinations = [diag for diag in combinations if len(diag) >= self._win_len]
        combinations.extend(
            it.chain.from_iterable([GomokuEnv.comb(diag, self._win_len) for diag in combinations])
        )
        combinations.extend(
            it.chain.from_iterable(GomokuEnv.comb(row.tolist(), self._win_len) for row in self._field)
        )
        combinations.extend(
            it.chain.from_iterable(GomokuEnv.comb(row.tolist(), self._win_len) for row in np.transpose(self._field))
        )

        combinations = [set(_) for _ in combinations if len(_) == self._win_len]

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
        result_str += "-\t" * (self._size + 2) + "\n\n"
        print(result_str)

    def available_turns(self):
        x_idx, y_idx = np.where(self._field == GomokuEnv.NOBODY)
        return list(zip(x_idx, y_idx))
