items = [1, 2, 3, 4, 5]
assert map(lambda x: x ** 2, items) == [1, 4, 9, 16, 25]

assert filter(lambda x: x > 2, items) == [3, 4, 5]

# assert reduce(lambda x, y: x * y, items) == 120
