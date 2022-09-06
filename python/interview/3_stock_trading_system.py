"""
时间复杂度O(n)
空间复杂度O(1)

思路:
遍历价格
1. 获取第一次买的最小成本
2. 获取第一次卖的最大收益
3. 获取第二次买的最小成本，第二次买的最小成本基于第一次卖的最大收益
4. 获取第二次卖的最大收益
"""

import sys


def get_max_profit(prices):
    first_buy_min_cost = sys.maxint
    second_buy_min_cost = sys.maxint

    first_sell_max_profit = -sys.maxint
    second_sell_max_profit = -sys.maxint

    for price in prices:
        # 第一次买的最小成本
        first_buy_min_cost = min(first_buy_min_cost, price)
        # 第一次卖的最大收益
        first_sell_max_profit = max(first_sell_max_profit, price - first_buy_min_cost)
        # 第二次买的最小成本
        second_buy_min_cost = min(second_buy_min_cost, price - first_sell_max_profit)
        # 第二次卖的最大收益
        second_sell_max_profit = max(
            second_sell_max_profit, price - second_buy_min_cost
        )

    return second_sell_max_profit


if __name__ == "__main__":
    assert get_max_profit([1, 2, 3, 4, 5, 6]) == 5
    assert get_max_profit([3, 3, 5, 0, 0, 3, 1, 4]) == 6
