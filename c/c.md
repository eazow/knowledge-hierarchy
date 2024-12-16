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

