import random
from collections import defaultdict
from typing import Dict, List

from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import min_weight_full_bipartite_matching

from mcmahon.constants import (
    AVOID_DUPLICATE_GAME,
    MINIMIZE_SCORE_DIFFERENCE,
    MAXIMIZE_SEEDING,
    BALANCE_FLOATING,
    BALANCE_COLORS,
)
from mcmahon.helpers import (
    cross_pairing,
    fold_pairing,
    adjacent_pairing,
    close_to_top,
    close_to_middle,
    close_to_bottom,
)
from mcmahon.parameters import PairingMode, FloatingMode
from mcmahon.participant import Participant, Participation
from mcmahon.game import Game


PAIRING_FUNCTIONS: Dict[PairingMode, callable] = {
    PairingMode.CROSS: cross_pairing,
    PairingMode.FOLD: fold_pairing,
    PairingMode.ADJACENT: adjacent_pairing,
}


FLOATING_FUNCTIONS: Dict[FloatingMode, callable] = {
    FloatingMode.TOP: close_to_top,
    FloatingMode.MIDDLE: close_to_middle,
    FloatingMode.BOTTOM: close_to_bottom,
}


class Tournament:
    def __init__(
        self,
        number_of_rounds: int = 5,
        mm_floor: int = -20,
        mm_bar: int = 8,
        mm_dense: bool = True,
        handicap_max: int = 9,
        handicap_bar: int = -30,
        handicap_correction: int = -2,
        pairing_mode: PairingMode = PairingMode.CROSS,
        draw_up_mode: FloatingMode = FloatingMode.MIDDLE,
        draw_down_mode: FloatingMode = FloatingMode.MIDDLE,
    ):
        self.number_of_rounds = number_of_rounds
        self.mm_floor = mm_floor
        self.mm_bar = mm_bar
        self.mm_dense = mm_dense
        self.handicap_max = handicap_max
        self.handicap_bar = handicap_bar
        self.handicap_correction = handicap_correction
        self.pairing_mode = pairing_mode
        self.draw_up_mode = draw_up_mode
        self.draw_down_mode = draw_down_mode

        self.participants = []
        self.games = []
        self._score_groups: Dict[int, list] = {}
        self._scores: defaultdict[Participant, Dict[int, int]] = defaultdict(dict)

    def add_participant(self, participant: Participant):
        if participant in self.participants:
            raise Exception(f"participant {participant} already added")
        self.participants.append(participant)
        for r in range(self.number_of_rounds):
            participant.participation.setdefault(r, Participation.UNKNOWN)

    def remove_participant(self, p: Participant):
        if p not in self.participants:
            raise Exception(f"participant {p} already removed")
        if any(g.has_participant(p) for g in self.games):
            raise Exception(f"participant {p} already played a game")
        self.participants.remove(p)

    def reset_start_mms(self):
        ranks = sorted(
            {
                p.rank
                for p in self.participants
                if self.mm_floor <= p.rank <= self.mm_bar
            }
        )

        for participant in self.participants:
            rank = min(max(ranks), max(participant.rank, min(ranks)))
            if self.mm_dense:
                participant.start_mms = ranks.index(rank)
            else:
                participant.start_mms = rank - min(ranks)

    def get_participant_games(self, participant: Participant, rn: int) -> List[Game]:
        return [
            game
            for game in self.games
            if game.has_participant(participant) and game.round_number <= rn
        ]

    def color_balance(self, participant: Participant, rn: int) -> int:
        return sum(
            game.color_balance(participant)
            for game in self.get_participant_games(participant, rn - 1)
        )

    def make_game(self, upper: Participant, lower: Participant, rn: int) -> Game:
        if upper.rank < upper.rank:
            upper, lower = lower, upper

        upper_rank = min(upper.rank, self.handicap_bar)
        lower_rank = min(lower.rank, self.handicap_bar)

        handicap = max(0, upper_rank - lower_rank + self.handicap_correction)

        upper_balance = self.color_balance(upper, rn)
        lower_balance = self.color_balance(lower, rn)

        if handicap > 0:
            white, black = upper, lower
        elif upper_balance < lower_balance:
            white, black = upper, lower
        elif upper_balance > lower_balance:
            white, black = lower, upper
        else:
            random.seed(hash(upper) + hash(lower))
            white, black = random.sample([upper, lower], k=2)

        return Game(
            white=white,
            black=black,
            handicap=min(self.handicap_max, handicap),
            round_number=rn,
        )

    def add_game(self, game: Game):
        if game in self.games:
            raise Exception("Game already added")

        self.games.append(game)

    def sorted_participants(self, rn: int) -> List[Participant]:
        return sorted(
            self.participants,
            key=lambda participant: [
                self.get_score_x2(participant, rn),
                participant.rank,
            ],
        )

    def participants_to_pair(self, rn: int) -> List[Participant]:
        return [
            p
            for p in self.sorted_participants(rn)
            if not p.participation[rn].is_absent_or_bye()
        ]

    def make_pairing(self, rn: int):

        participants_to_pair = self.participants_to_pair(rn)

        number_of_participants = len(participants_to_pair)
        costs = csr_matrix((number_of_participants, number_of_participants))

        for i in range(1, number_of_participants):
            for j in range(i - 1):
                costs[i, j] = costs[j, i] = self.cost_value(
                    participants_to_pair[i],
                    participants_to_pair[j],
                    rn,
                )

        match = min_weight_full_bipartite_matching(costs, maximize=True)

        paired = set()
        pairs = []
        for i, j in zip(*match):
            if i not in paired and j not in paired:
                p1 = participants_to_pair[i]
                p2 = participants_to_pair[j]
                game = self.make_game(p1, p2, rn)
                self.add_game(game)
                pairs.append((i, j))
                paired.add(i)
                paired.add(j)

    def _avoid_duplicate_game_cost(
        self,
        p1: Participant,
        p2: Participant,
        rn: int,
    ) -> float:
        """Base Criterion 1 : Avoid Duplicating Game"""
        for game in self.get_participant_games(p1, rn - 1):
            if game.opponent(p1) is p2:
                return 0
        for game in self.get_participant_games(p2, rn - 1):
            if game.opponent(p2) is p1:
                return 0
        return AVOID_DUPLICATE_GAME

    def _balance_colors_cost(self, p1: Participant, p2: Participant, rn: int) -> float:
        """Base Criterion 2 : Balance Colors"""
        game = self.make_game(p1, p2, rn)

        coef = 0
        if not game.handicap:
            p1_balance = self.color_balance(p1, rn)
            p2_balance = self.color_balance(p2, rn)
            if p1_balance * p2_balance < 0:
                coef = 2  # corrects color balance for both participants
            elif p1_balance * p2_balance == 0:
                if abs(p1_balance) > 1 or abs(p2_balance) > 1:
                    coef = 1  # corrects color balance for one participant

        return BALANCE_COLORS * coef

    def _minimize_score_difference_cost(
        self,
        p1: Participant,
        p2: Participant,
        rn: int,
    ) -> float:
        """Main Criterion 1 : Minimize score difference"""
        score_groups = sorted(
            {self.get_score_x2(p, rn - 1) for p in self.participants_to_pair(rn)}
        )
        p1_group = score_groups.index(self.get_score_x2(p1, rn - 1))
        p2_group = score_groups.index(self.get_score_x2(p2, rn - 1))

        x = abs(p1_group - p2_group) / len(score_groups)
        return MINIMIZE_SCORE_DIFFERENCE * (1 - x) * (1 + x / 2)

    def draw_ups(self, participant: Participant, rn: int):
        score_x2 = self.get_score_x2(participant, rn)
        return len(
            [
                game
                for game in self.get_participant_games(participant, rn)
                if self.get_score_x2(game.opponent(participant), rn) > score_x2
            ]
        )

    def draw_downs(self, participant: Participant, rn: int):
        score_x2 = self.get_score_x2(participant, rn)
        return len(
            [
                game
                for game in self.get_participant_games(participant, rn)
                if self.get_score_x2(game.opponent(participant), rn) < score_x2
            ]
        )

    def _balance_floatings_cost(
        self,
        upper: Participant,
        lower: Participant,
        rn: int,
    ) -> float:
        """Main Criterion 2 : Balance Floatings"""

        if self.get_score_x2(upper, rn) < self.get_score_x2(lower, rn):
            lower, upper = upper, lower

        score_groups = sorted(
            {self.get_score_x2(p, rn - 1) for p in self.participants_to_pair(rn)}
        )
        upper_group = score_groups.index(self.get_score_x2(upper, rn - 1))
        lower_group = score_groups.index(self.get_score_x2(lower, rn - 1))

        lower_draw_ups = self.draw_ups(lower, rn)
        lower_draw_downs = self.draw_downs(lower, rn)
        upper_draw_ups = self.draw_ups(upper, rn)
        upper_draw_downs = self.draw_downs(upper, rn)

        scenario = 2  # normal conditions
        if upper_group < lower_group:

            if lower_draw_ups:
                scenario -= 1  # increases lower participant draw ups
            if upper_draw_downs:
                scenario -= 1  # increases upper participant draw downs

            if scenario > 0:  # if not the worst case
                if lower_draw_ups < lower_draw_downs:
                    scenario += 1  # corrects lower participant draw ups
                if upper_draw_downs < upper_draw_ups:
                    scenario += 1  # corrects upper participant draw downs

        return BALANCE_FLOATING * scenario

    def get_participant_group(self, participant: Participant, rn) -> List[Participant]:
        score_x2 = self.get_score_x2(participant, rn)
        return [
            participant
            for participant in self.sorted_participants(rn)
            if self.get_score_x2(participant, rn) == score_x2
        ]

    def _seeding_cost(self, upper: Participant, lower: Participant, rn: int) -> float:
        """Main Criterion 3 : Seeding"""
        if self.get_score_x2(upper, rn) < self.get_score_x2(lower, rn):
            lower, upper = upper, lower

        upper_group = self.get_participant_group(upper, rn - 1)
        lower_group = self.get_participant_group(lower, rn - 1)

        upper_place = upper_group.index(upper)
        lower_place = lower_group.index(lower)

        if upper_group == lower_group:
            pairing_func = PAIRING_FUNCTIONS[self.pairing_mode]
            coef = pairing_func(upper_place, lower_place, len(upper_group))
        else:
            upper_floating_func = FLOATING_FUNCTIONS[self.draw_down_mode]
            lower_floating_func = FLOATING_FUNCTIONS[self.draw_up_mode]
            upper_coef = upper_floating_func(upper_place, len(upper_group))
            lower_coef = lower_floating_func(lower_place, len(lower_group))
            coef = (upper_coef + lower_coef) / 2
        return MAXIMIZE_SEEDING * coef

    def cost_value(
        self,
        p1: Participant,
        p2: Participant,
        rn: int,
    ) -> float:
        cost = 0.0

        # Base criteria
        cost += self._avoid_duplicate_game_cost(p1, p2, rn)
        cost += self._balance_colors_cost(p1, p2, rn)

        # Main criteria
        cost += self._minimize_score_difference_cost(p1, p2, rn)
        cost += self._balance_floatings_cost(p1, p2, rn)
        cost += self._seeding_cost(p1, p2, rn)

        return cost

    def _set_score(self, participant: Participant, rn: int):
        score_x2 = participant.start_mms
        for game in self.get_participant_games(participant, rn):
            score_x2 += game.points_x2(participant)

        score_x2 += participant.absent_or_bye_x2(rn)

        self._scores[participant][rn] = score_x2

    def get_score_x2(self, participant: Participant, rn: int) -> int:
        if participant not in self._scores or rn not in self._scores[participant]:
            self._set_score(participant, rn)
        return self._scores[participant][rn]

    def get_sos_x2(self, participant: Participant, rn: int) -> int:
        sos_x2 = 0
        for game in self.get_participant_games(participant, rn):
            score_x2 = self.get_score_x2(game.opponent(participant), rn)
            sos_x2 += score_x2
        return sos_x2

    def get_sodos_x2(self, participant: Participant, rn: int) -> int:
        sodos_x2 = 0
        for game in self.get_participant_games(participant, rn):
            if game.is_winner(participant):
                score_x2 = self.get_score_x2(game.opponent(participant), rn)
                sodos_x2 += score_x2
        return sodos_x2

    def get_sosos_x2(self, participant: Participant, rn: int):
        sosos_x2 = 0
        for game in self.get_participant_games(participant, rn):
            sos_x2 = self.get_sos_x2(game.opponent(participant), rn)
            sosos_x2 += sos_x2
        return sosos_x2
