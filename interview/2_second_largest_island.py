# -*- coding: utf-8 -*-
# 时间复杂度O(n的平方)
# 空间复杂度O(2的n次方)，因为需要采用了递归的方式计算小岛面积
#
# 思路：
# 1. 找出上、下、左、右都有1的0，将其标记为9，表示要计算面积的小岛
# 2. 遍历matrxi，找到9，递归计算该小岛上、下、左、右连接小岛的面积，面积+1后，将9替换为-1，表示该小岛已计算过面积



def find_land(matrix):
    """
    找到每一行最左边陆地的位置，最右边陆地的位置
    找到每一列最上边陆地的位置，最下边陆地的位置
    用于判断matrix[i][j]
    :param matrix:
    :return:
    """
    row_land_positions = [[-1, -1] for i in range(len(matrix))] * len(matrix)
    col_land_positions = [[-1, -1] for j in range(len(matrix[0]))]

    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == 1:
                if row_land_positions[i][0] == -1:
                    row_land_positions[i][0] = j
                row_land_positions[i][1] = j

                if col_land_positions[j][0] == -1:
                    col_land_positions[j][0] = i
                col_land_positions[j][1] = i


    return row_land_positions, col_land_positions

def calculate_area(matrix, i, j):
    """
    计算一个小岛面积
    :param matrix:
    :param i:
    :param j:
    :return:
    """
    if 0 <= i < len(matrix) and 0 <=j < len(matrix[0]) and matrix[i][j] == 9:
        # 将值修改为-1，表示已经计算果面积
        matrix[i][j] = -1
        return 1 + calculate_area(matrix, i+1, j) + calculate_area(matrix, i, j+1) \
                + calculate_area(matrix, i-1, j) + calculate_area(matrix, i, j-1)
    return 0


def calculate_all_areas(matrix):
    """
    计算所有小岛面积，并排序后存入areas中
    :param matrix:
    :return: list
    """
    areas = []
    for i in range(0, len(matrix)):
        for j in range(0, len(matrix[0])):
            if matrix[i][j] == 9:
                areas.append(calculate_area(matrix, i, j))

    areas.sort(reverse=True)
    return areas


def mark_island(matrix):
    """
    标记小岛
    将被1包围的小岛标记为9
    :param matrix:
    :return:
    """
    row_land_positions, col_land_positions = find_land(matrix)

    rows = len(matrix)
    cols = 0
    if rows > 0:
        cols = len(matrix[0])

    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            if matrix[i][j] == 0 and (row_land_positions[i][0] < j < row_land_positions[i][1]) \
                    and (col_land_positions[j][0] < i < col_land_positions[j][1]):
                matrix[i][j] = 9


def find_second_largest_island(matrix):
    """
    找出第二大岛，如果没有第二大岛，则返回第一大岛
    :param matrix:
    :return:
    """
    mark_island(matrix)

    areas = calculate_all_areas(matrix)
    return areas[1] if len(areas) > 1 else areas[0]



if __name__ == '__main__':
    matrix = [
        [1, 1, 1, 1, 1, 1],
        [1, 1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1, 0],
        [1, 1, 0, 1, 1, 1],
        [0, 1, 0, 1, 0, 0],
        [1, 1, 1, 1, 1, 1]
    ]

    assert find_second_largest_island(matrix) == 8

    matrix = [
        [1, 1, 1, 1, 1],
        [1, 1, 0, 0, 0],
        [1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1],
        [0, 1, 0, 1, 0],
        [1, 1, 1, 1, 1]
    ]

    assert find_second_largest_island(matrix) == 1