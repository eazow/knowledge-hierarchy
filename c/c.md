### printf
char message[] = "Hello, World!";
printf("%s\n", message);


### malloc
```
#include <stdlib.h>
int main() {
    int i = 0
    while(i++ < 100) {
        malloc(1024*1024); // 分配1MB内存
    }
    return 0;
}
```


### memcpy
```
#include <string.h>

// 基本用法
void example_memcpy() {
    char src[] = "Hello";
    char dest[6];
    memcpy(dest, src, 6);  // 包含结尾的'\0'
    
    // 复制结构体
    struct Person {
        int age;
        char name[20];
    };
    struct Person p1 = {25, "Tom"};
    struct Person p2;
    memcpy(&p2, &p1, sizeof(struct Person));
}
```


### memset
```
// 清零
int array[100];
memset(array, 0, sizeof(array));

// 初始化结构体
struct Data {
    int a;
    float b;
} data;
memset(&data, 0, sizeof(struct Data));


```


### memmove
```
char str[] = "Hello World";
memmove(str+1, str, 5);  // 安全处理重叠区域
```


### memcmp
```
char buf1[] = "Hello";
char buf2[] = "Hello";
int result = memcmp(buf1, buf2, 5);  // 返回0表示相等
```


### 字符串操作
```
strlen()   // 字符串长度
strcpy()   // 字符串复制
strncpy()  // 安全字符串复制
strcat()   // 字符串连接
strncat()  // 安全字符串连接
strcmp()   // 字符串比较
strncmp()  // 安全字符串比较
```

### 内存分配
```
malloc()   // 分配内存
calloc()   // 分配并清零
realloc()  // 重新分配内存
free()     // 释放内存
```


### 文件操作
```
fread()    // 文件读取
fwrite()   // 文件写入
fseek()    // 文件定位
ftell()    // 获取文件位置
```

#### ex1
```
#include <stdio.h>
#include <string.h>

void safe_memory_ops() {
    char src[100] = "Source data";
    char dest[100];
    size_t src_len = strlen(src) + 1;
    
    // 检查缓冲区大小
    if (sizeof(dest) >= src_len) {
        memcpy(dest, src, src_len);
    }
    
    // 使用strncpy替代strcpy
    strncpy(dest, src, sizeof(dest) - 1);
    dest[sizeof(dest) - 1] = '\0';
}
```


### 注意事项
- 始终检查内存边界
- 注意内存对齐
- 处理NULL指针
- 考虑使用安全版本的函数
- 注意内存泄漏





## 高级使用

### 函数指针

```
// 函数指针定义和使用
typedef int (*operation)(int, int);

int add(int a, int b) { return a + b; }
int subtract(int a, int b) { return a - b; }

// 使用函数指针数组
operation ops[] = {add, subtract};
int result = ops[0](10, 5);  // 调用add
```



### 指针数组和数组指针

```
// 指针数组
char *names[] = {"John", "Mary", "Tom"};

// 数组指针
int (*matrix)[4];  // 指向含4个整数的数组的指针
```



### 内存管理

#### 动态内存分配

```
// 内存分配和释放
void *memory_manager() {
    // 分配内存
    int *array = (int*)malloc(sizeof(int) * 10);
    if (!array) return NULL;
    
    // 重新分配
    array = (int*)realloc(array, sizeof(int) * 20);
    
    // 释放内存
    free(array);
    return NULL;
}
```

#### 内存对齐

```
// 结构体对齐
#pragma pack(push, 1)  // 设置1字节对齐
struct packed_struct {
    char c;
    int i;
    double d;
};
#pragma pack(pop)
```





### 查看.so

**nm(name mangling 或 name mapping) ** 

name list of symbols

显示目标文件（object file）中的符号信息

```
# 查看所有符号
nm -D libxxx.so

# 只查看导出的符号
nm -gD libxxx.so

# 带类型信息查看
nm -gDC libxxx.so

```

**使用 objdump 命令**

```
# 查看所有信息
objdump -T libxxx.so

# 查看详细反汇编
objdump -d libxxx.so

# 查看动态符号表
objdump -tT libxxx.so
```

**使用 readelf 命令**

```
# 查看符号表
readelf -s libxxx.so

# 查看动态符号表
readelf --dyn-syms libxxx.so

# 查看所有头信息
readelf -a libxxx.so
```



### coredump

Segmentation Fault (段错误):

- 是一种程序运行时错误
- 发生在程序访问非法内存地址时
- 常见原因：
  1. 访问空指针
  2. 访问已释放的内存
  3. 数组越界
  4. 栈溢出
  5. 访问只读内存区域

Coredump (核心转储):

- 是程序崩溃时产生的内存快照文件
- 包含程序崩溃时的状态信息
- 可由多种错误触发，Segmentation Fault 只是其中之一
- 其他可能导致 Coredump 的原因：
  1. 断言失败（assert）
  2. 未捕获的异常
  3. 程序主动调用 abort()
  4. 收到特定信号（如 SIGSEGV, SIGABRT）
