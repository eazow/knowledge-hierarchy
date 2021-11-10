def fibon(n):
    a = b = 1
    for i in range(n):
        yield a
        a, b = b, a + b


for x in fibon(10000):
    print(x)

gen = fibon(100)
print(next(gen))
print(next(gen))


my_string = "Yasoob"
my_iter = iter(my_string)
assert next(my_iter) == "Y"
