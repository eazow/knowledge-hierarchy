# -*- coding:utf-8 -*-
import pytest
from shopping_cart.shopping import Customer

def test_invalid_input1():
    input_case2 = u"""\
2019.6.14 | 0.7 | abc
2019.6.14 | 0.8 | 日用品
2019.6.18 | 0.1 | 食品

1 * iPad: 1000.00
12 * 啤酒: 10.00
8 * 餐巾纸: 1.00
3 * 蔬菜: 10.00

2019.6.14
"""
    total_price = Customer().shopping_and_settle(input_case2)
    assert total_price == "Wrong category"


def test_invalid_input2():
    input_case2 = u"""\
2019.6.14 | 0.8 | 日用品
2019.6.18 | 0.1 | 食品

1 * iPad: 1000.00
12 * 啤酒ab: 10.00
8 * 餐巾纸: 1.00
3 * 蔬菜: 10.00

2019.6.14
"""
    total_price = Customer().shopping_and_settle(input_case2)
    assert total_price == "Wrong product name"


def test_invalid_input3():
    input_case3 = u"""\
2019.6.14 | 0.7a | 电子
2019.6.14 | 0.8 | 日用品
2019.6.18 | 0.1 | 食品

1 * iPad: 1000.00
12 * 啤酒: 10.00
8 * 餐巾纸: 1.00
3 * 蔬菜: 10.00

2019.6.14
"""
    total_price = Customer().shopping_and_settle(input_case3)
    assert total_price == u"Wrong line: 2019.6.14 | 0.7a | 电子"
