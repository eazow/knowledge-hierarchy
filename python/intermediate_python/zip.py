# -*- coding:utf-8 -*-

a = [1, 2, 3]
b = [4, 5, 6]

assert zip(a, b) == [(1, 4), (2, 5), (3, 6)]

# 注意*号
assert zip(*zip(a, b)) == [(1, 2, 3), (4, 5, 6)]