# -*- coding:utf-8 -*-
from shopping_cart.shopping import Customer


def test_case1():
    input_case1 = u"""\
2013.11.11 | 0.7 | 电子

1 * iPad: 2399.00
1 * 显示器: 1799.00
12 * 啤酒: 25.00
5 * 面包: 9.00

2013.11.11
2014.3.2 | 1000 | 200
"""
    total_price = Customer().shopping_and_settle(input_case1)
    assert total_price == "3083.60"


def test_case2():
    input_case2 = u"""\
2019.6.14 | 0.7 | 电子
2019.6.14 | 0.8 | 日用品
2019.6.18 | 0.1 | 食品

1 * iPad: 1000.00
12 * 啤酒: 10.00
8 * 餐巾纸: 1.00
3 * 蔬菜: 10.00

2019.6.14
"""
    total_price = Customer().shopping_and_settle(input_case2)
    assert total_price == "856.40"


