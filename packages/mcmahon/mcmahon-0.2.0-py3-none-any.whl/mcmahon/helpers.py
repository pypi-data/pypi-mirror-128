def cross_pairing(
    p1_placement: int,
    p2_placement: int,
    group_size: int,
) -> float:
    """
    Split and Slip (Cross Pairing)
    :param p1_placement: should be in range(0, group_size)
    :param p2_placement: should be in range(0, group_size)
    :param group_size: number of players in group
    :return:
    """
    x = 2 * abs(p1_placement - p2_placement) - group_size
    return 1 - (x / group_size) ** 2


def fold_pairing(
    p1_placement: int,
    p2_placement: int,
    group_size: int,
) -> float:

    """
    Split and Fold (Slaughter Pairing)
    :param p1_placement: should be in range(0, group_size)
    :param p2_placement: should be in range(0, group_size)
    :param group_size: number of players in group
    :return:
    """
    x = group_size - 1 - (p1_placement + p2_placement)
    return 1 - (x / group_size) ** 2


def adjacent_pairing(
    p1_placement: int,
    p2_placement: int,
    group_size: int,
) -> float:
    """
    K
    :param p1_placement: should be in range(0, group_size)
    :param p2_placement: should be in range(0, group_size)
    :param group_size: number of players in group
    :return:
    """
    x = abs(p1_placement - p2_placement) - 1
    return 1 - (x / group_size) ** 2


def close_to_middle(placement: int, group_size: int) -> float:
    """
    :param placement: should be in range(0, group_size)
    :param group_size: number of players in group
    :return: 1 if right in the middle
    """
    if placement < 0 or placement >= group_size:
        return 0.0

    x = abs(2 * placement - group_size + 1)
    return 1 - (x / group_size) ** 2


def close_to_top(placement: int, group_size: int) -> float:
    """
    :param placement: should be in range(0, group_size)
    :param group_size: number of players in group
    :return:
    """
    if placement < 0 or placement >= group_size:
        return 0.0

    return 1 - (placement / group_size) ** 2


def close_to_bottom(placement: int, group_size: int) -> float:
    """
    :param placement: should be in range(0, group_size)
    :param group_size: number of players in group
    :return: coefficient of closeness to bottom
    """
    if placement < 0 or placement >= group_size:
        return 0.0

    x = placement + 1 - group_size
    return 1 - (x / group_size) ** 2


def rank_to_rating(rank: int) -> int:
    if rank < -30:
        return 0
    if rank < -20:
        return (rank + 30) * 10
    return (rank + 21) * 100


def rank_to_grade(rank: int) -> str:
    if rank < 0:
        return f"{-rank:d}k"
    return f"{rank:d}d"
