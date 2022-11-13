
def optimize(club_levels, months_count):
    """
    每个月找出水平最高的俱乐部, 减掉3个战斗力，补充给其他3个队，每队+1个战斗力
    :param club_levels: 俱乐部水平, 数组
    :param months_count: 优化经历的月份数
    :return: 优化后的俱乐部水平
    """
    for _ in range(months_count):
        max_level = max(club_levels)

        club_levels = [level - 3 if level == max_level else level + 1 for level in club_levels]

    return club_levels


def get_max_and_index(levels):
    max_level = max(levels)
    return max(levels), levels.index(max_level)


if __name__ == '__main__':
    club_levels = [10, 7, 5, 4]

    assert optimize(club_levels, 1) == [7, 8, 6, 5]

    assert optimize(club_levels, 12 * 5) == [6, 7, 5, 8]
    # 5年即60个月后，第4个队(index=3)战斗力最高，为8
    assert get_max_and_index(optimize(club_levels, 12 * 5)) == (8, 3)
