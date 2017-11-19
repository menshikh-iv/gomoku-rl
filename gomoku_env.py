import itertools as it
import numpy as np
import copy


class BoardState(object):
    NOBODY = 0
    X = 1
    O = 2
    DRAW = 3

    def __init__(self, board_size, win_len):
        assert board_size >= 3
        assert win_len >= 3
        assert win_len <= board_size

        self.field = None
        self.current_step = BoardState.X
        self.size = board_size
        self.win_len = win_len
        self.reset()

    def reset(self):
        self.field = np.zeros((self.size, self.size), dtype=int)

    def available_turns(self):
        x_idx, y_idx = np.where(self.field == BoardState.NOBODY)
        return list(zip(x_idx, y_idx))

    def render(self):
        result_str = "Next turn - `{}`\n".format("X" if self.current_step == BoardState.X else "O")
        result_str += "-\t" * (self.size + 2) + "\n"
        for row in self.field:
            result_str += "|\t"
            for el in row:
                if el == BoardState.NOBODY:
                    result_str += ".\t"
                    continue
                result_str += "X\t" if el == BoardState.X else "O\t"
            result_str += "|\n"
        result_str += "-\t" * (self.size + 2) + "\n\n"
        return result_str


class GomokuEnv(object):

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
        self.state = BoardState(board_size, win_len)

    def reset(self):
        return self.state.reset()

    def render(self):
        return self.state.render()

    def available_turns(self):
        return self.state.available_turns()

    def getstate(self):
        return copy.deepcopy(self.state)

    def step(self, player, action):
        if player not in {BoardState.X, BoardState.O}:
            raise ValueError("Incorrect player {} (must be {} or {})".format(player, BoardState.X, BoardState.O))

        if player != self.state.current_step:
            raise ValueError("Incorrect player {}, now it's {} turn".format(player, self.state.current_step))

        x, y = action
        if x >= self.state.size or y >= self.state.size or x < 0 or y < 0:
            raise ValueError("Action {} out of field ({} X {})".format(action, self.state.size, self.state.size))

        if self.state.field[x][y] != BoardState.NOBODY:
            raise RuntimeError("Incorrect move {}, this cell already filled".format(action))

        self.state.field[x][y] = player
        self.state.current_step = BoardState.X if player == BoardState.O else BoardState.O
        return self.getstate(), self._who_is_winner()

    def _who_is_winner(self):
        combinations = GomokuEnv.get_all_diags(self.state.field)
        combinations = [diag for diag in combinations if len(diag) >= self.state.win_len]
        combinations.extend(
            it.chain.from_iterable([GomokuEnv.comb(diag, self.state.win_len) for diag in combinations])
        )
        combinations.extend(
            it.chain.from_iterable(GomokuEnv.comb(row.tolist(), self.state.win_len) for row in self.state.field)
        )
        combinations.extend(
            it.chain.from_iterable(
                GomokuEnv.comb(row.tolist(), self.state.win_len) for row in np.transpose(self.state.field)
            )
        )

        combinations = [set(_) for _ in combinations if len(_) == self.state.win_len]

        if {BoardState.O} in combinations:
            return BoardState.O

        if {BoardState.X} in combinations:
            return BoardState.X

        if np.count_nonzero(self.state.field) == self.state.size * self.state.size:
            return BoardState.DRAW

        return BoardState.NOBODY
