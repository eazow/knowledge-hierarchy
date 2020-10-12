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



class Logit(object):
    def __init__(self, logfile='out.log'):
        self.logfile = logfile

    def __call__(self, func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            log_string = func.__name__ + " was called"
            print(log_string)

            with open(self.logfile, 'a') as opened_file:
                opened_file.write(log_string + "\n")

            self.notify()
            return func(*args, **kwargs)

        return wrapped_function

    def notify(self):
        pass


@Logit()
def my_func():
    print("in my func")


my_func()
