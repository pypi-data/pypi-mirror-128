from enum import Enum

from mcmahon.player import Player


class Result(str, Enum):
    UNKNOWN = "unknown"
    WHITE_WINS = "white_wins"
    BLACK_WINS = "black_wins"
    DRAW = "draw"
    BOTH_WIN = "both_win"
    BOTH_LOSE = "both_lose"

    def known(self) -> bool:
        return self is not self.UNKNOWN

    def white_wins(self) -> bool:
        return self in [self.WHITE_WINS, self.BOTH_WIN]

    def black_wins(self) -> bool:
        return self in [self.BLACK_WINS, self.BOTH_WIN]

    def white_lose(self) -> bool:
        return self in [self.BLACK_WINS, self.BOTH_LOSE]

    def black_lose(self) -> bool:
        return self in [self.WHITE_WINS, self.BOTH_LOSE]

    def draw(self) -> bool:
        return self is self.DRAW

    def score_string(self, white_first: bool = True, by_default: bool = False):
        if self.draw():
            return "½-½"
        wr = int(self.white_wins())
        br = int(self.black_wins())
        result = f"{wr}-{br}" if white_first else f"{br}-{wr}"
        if by_default:
            result += "!"
        return result


class Game:
    def __init__(
        self,
        white: Player,
        black: Player,
        round_number: int,
        handicap: int = 0,
        result: Result = Result.UNKNOWN,
        by_default: bool = False,
    ):
        self.white = white
        self.black = black
        self.round_number = round_number
        self.handicap = handicap
        self.result = result
        self.by_default = by_default

    def has_player(self, player: Player) -> bool:
        return self.white is player or self.black is player

    def is_winner(self, player: Player) -> bool:
        if player == self.white:
            return self.result.white_wins()
        if player == self.black:
            return self.result.black_wins()
        return False

    def is_draw(self) -> bool:
        return self.result.draw()

    def points_x2(self, player: Player, virtual: bool = False) -> int:
        if self.by_default and virtual:
            return 1

        if self.is_winner(player):
            return 2

        if self.is_draw():
            return 1

        return 0

    def opponent(self, player: Player) -> Player:
        if self.white is player:
            return self.black
        if self.black is player:
            return self.white

    def color_balance(self, player: Player):
        if self.handicap:
            return 0
        if self.white is player:
            return 1
        if self.black is player:
            return -1
        return 0
