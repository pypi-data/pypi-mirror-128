from enum import Enum


class PairingMode(str, Enum):
    CROSS = "cross"
    FOLD = "fold"
    ADJACENT = "adjacent"


class FloatingMode(str, Enum):
    TOP = "top"
    MIDDLE = "middle"
    BOTTOM = "bottom"
