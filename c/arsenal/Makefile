CC = gcc
CFLAGS = -Wall -Wextra -std=c99 -g
UNITY_ROOT = ./unity

# 源文件
SOURCES = binary_search.c
TEST_SOURCES = test_binary_search.c
UNITY_SOURCES = $(UNITY_ROOT)/src/unity.c

# 目标文件
OBJECTS = $(SOURCES:.c=.o)
TEST_OBJECTS = $(TEST_SOURCES:.c=.o)
UNITY_OBJECTS = $(UNITY_SOURCES:.c=.o)

# 可执行文件
TEST_TARGET = test_runner

all: test

# 编译测试
test: $(TEST_TARGET)
	./$(TEST_TARGET)

$(TEST_TARGET): $(OBJECTS) $(TEST_OBJECTS) $(UNITY_OBJECTS)
	$(CC) $(CFLAGS) -o $@ $^ -I$(UNITY_ROOT)/src

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@ -I$(UNITY_ROOT)/src

clean:
	rm -f *.o $(TEST_TARGET)

.PHONY: all test clean
