def fibonacci(n):
    a = b = 1
    for i in range(n):
        yield a
        a, b = b, a + b


for x in fibonacci(10000):
    print(x)

gen = fibonacci(100)
print(next(gen))
print(next(gen))


my_string = "Yasoob"
my_iter = iter(my_string)
assert next(my_iter) == "Y"
