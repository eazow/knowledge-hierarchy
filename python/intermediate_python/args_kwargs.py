# -*- coding:utf-8 -*-

def my_var_args(f_arg, *args):
    print("first normal arg: ", f_arg)
    for arg in args:
        print("another arg through *args: ", arg)


my_var_args("yasoob", "python", "eggs", "test")


def greet_me(**kwargs):
    for key, value in kwargs.items():
        print("{0} == {1}").format(key, value)


greet_me(name="yasoob")
