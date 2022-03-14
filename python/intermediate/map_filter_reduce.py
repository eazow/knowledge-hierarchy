from functools import reduce

items = [1, 2, 3, 4, 5]

assert list(map(lambda x: x ** 2, items)) == [1, 4, 9, 16, 25]

assert list(filter(lambda x: x > 2, items)) == [3, 4, 5]

assert reduce(lambda x, y: x * y, items) == 120
