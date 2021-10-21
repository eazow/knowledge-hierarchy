# -*- coding:utf-8 -*-

# coroutine: 协程


def grep(pattern):
    print("Searching for", pattern)
    while True:
        line = (yield)
        if pattern in line:
            print(line)


# 发送的值会被yield接收。我们为什么要运行next()方法呢？这样做正是为了启动一个协程。
# 就像协程中包含的生成器并不是立刻执行，而是通过next()方法来响应send()方法。
# 因此，你必须通过next()方法来执行yield表达式。
search = grep('coroutine')
next(search)
#output: Searching for coroutine
search.send("I love you")
search.send("Don't you love me?")
search.send("I love coroutine instead!")
#output: I love coroutine instead!

search.close()