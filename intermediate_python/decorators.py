# -*- coding:utf-8 -*-
from functools import wraps


def a_new_docorator(a_func):
    @wraps(a_func)
    def wrap_the_function(*args, **kwargs):
        print("before a_func()")
        a_func(*args, **kwargs)
        print("after a_func()")

    return wrap_the_function


@a_new_docorator
def a_function_requiring_decoration(a, b):
    print("function which needs some decoration")
    print("arguments: %s, %s" % (a, b))


a_function_requiring_decoration("abc", b="def")

# the @a_new_decorator is just a short way of saying
# a_function_requiring_decoration = a_new_docorator(a_function_requiring_decoration)

# print wrap_the_function if there is not @wraps
print(a_function_requiring_decoration.__name__)