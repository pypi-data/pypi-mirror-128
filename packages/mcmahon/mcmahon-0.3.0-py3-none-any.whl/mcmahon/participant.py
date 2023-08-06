from typing import Dict
from enum import Enum


class Participation(str, Enum):
    UNKNOWN = "unknown"
    ABSENT = "absent"
    BYE = "bye"
    READY = "ready"
    PAIRED = "paired"

    def is_absent(self) -> bool:
        return self is self.ABSENT

    def is_bye(self) -> bool:
        return self is self.BYE

    def is_absent_or_bye(self) -> bool:
        return self in [self.ABSENT, self.BYE]

    def score_x2(self) -> int:
        if self.is_absent():
            return 1
        if self.is_bye():
            return 2
        return 0


class Participant:
    def __init__(
        self,
        last_name: str,
        first_name: str,
        country: str,
        rating: int,
        start_mms: int = 0,
        participation: Dict[int, Participation] = None,
        is_final: bool = False,
    ):
        self.last_name = last_name
        self.first_name = first_name
        self.country = country
        self.rating = rating
        self.start_mms = start_mms
        self.is_final = is_final

        self.participation = participation or {}

    def __eq__(self, other: "Participant"):
        return all(
            [
                self.country == other.country,
                self.last_name == other.last_name,
                self.first_name == other.first_name,
            ]
        )

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.country} [{self.rating}]"

    def __hash__(self):
        return hash(f"{self.country}_{self.last_name}_{self.first_name}")

    @property
    def rank(self) -> int:
        return self.rating // 100 - 21

    def absent_or_bye_x2(self, rn: int, round_down: bool = True) -> int:
        points = sum(
            [
                status.score_x2()
                for r, status in self.participation.items()
                if r <= rn and status.is_absent_or_bye()
            ]
        )

        if round_down:
            points -= points % 2

        return points
