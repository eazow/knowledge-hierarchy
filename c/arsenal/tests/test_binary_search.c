#include "unity.h"
#include "binary_search.h"

// 测试用的数组
static int sorted_array[] = {1, 3, 5, 7, 9, 11, 13, 15, 17, 19};
static int array_size = sizeof(sorted_array) / sizeof(sorted_array[0]);

void setUp(void) {
    // 每个测试前的初始化
}

void tearDown(void) {
    // 每个测试后的清理
}

// 测试找到目标值的情况
void test_binary_search_found_first_element(void) {
    int result = binary_search(sorted_array, array_size, 1);
    TEST_ASSERT_EQUAL_INT(0, result);
}

void test_binary_search_found_middle_element(void) {
    int result = binary_search(sorted_array, array_size, 9);
    TEST_ASSERT_EQUAL_INT(4, result);
}

void test_binary_search_found_last_element(void) {
    int result = binary_search(sorted_array, array_size, 19);
    TEST_ASSERT_EQUAL_INT(9, result);
}

// 测试未找到目标值的情况
void test_binary_search_not_found_too_small(void) {
    int result = binary_search(sorted_array, array_size, 0);
    TEST_ASSERT_EQUAL_INT(-1, result);
}

void test_binary_search_not_found_too_large(void) {
    int result = binary_search(sorted_array, array_size, 25);
    TEST_ASSERT_EQUAL_INT(-1, result);
}

void test_binary_search_not_found_between_elements(void) {
    int result = binary_search(sorted_array, array_size, 6);
    TEST_ASSERT_EQUAL_INT(-1, result);
}

// 测试边界情况
void test_binary_search_empty_array(void) {
    int empty_array[] = {};
    int result = binary_search(empty_array, 0, 5);
    TEST_ASSERT_EQUAL_INT(-1, result);
}

void test_binary_search_single_element_found(void) {
    int single_array[] = {42};
    int result = binary_search(single_array, 1, 42);
    TEST_ASSERT_EQUAL_INT(0, result);
}

void test_binary_search_single_element_not_found(void) {
    int single_array[] = {42};
    int result = binary_search(single_array, 1, 24);
    TEST_ASSERT_EQUAL_INT(-1, result);
}

// 测试递归版本
void test_binary_search_recursive_found(void) {
    int result = binary_search_recursive(sorted_array, 0, array_size - 1, 11);
    TEST_ASSERT_EQUAL_INT(5, result);
}

void test_binary_search_recursive_not_found(void) {
    int result = binary_search_recursive(sorted_array, 0, array_size - 1, 8);
    TEST_ASSERT_EQUAL_INT(-1, result);
}

// 性能测试（大数组）
void test_binary_search_large_array(void) {
    // 创建大数组进行性能测试
    const int large_size = 10000;
    static int large_array[10000];
    
    // 初始化大数组
    for (int i = 0; i < large_size; i++) {
        large_array[i] = i * 2;  // 偶数序列
    }
    
    // 测试查找存在的元素
    int result = binary_search(large_array, large_size, 1000);
    TEST_ASSERT_EQUAL_INT(500, result);
    
    // 测试查找不存在的元素
    result = binary_search(large_array, large_size, 999);
    TEST_ASSERT_EQUAL_INT(-1, result);
}

// Unity测试运行器
int main(void) {
    UNITY_BEGIN();
    
    // 基本功能测试
    RUN_TEST(test_binary_search_found_first_element);
    RUN_TEST(test_binary_search_found_middle_element);
    RUN_TEST(test_binary_search_found_last_element);
    
    // 未找到情况测试
    RUN_TEST(test_binary_search_not_found_too_small);
    RUN_TEST(test_binary_search_not_found_too_large);
    RUN_TEST(test_binary_search_not_found_between_elements);
    
    // 边界情况测试
    RUN_TEST(test_binary_search_empty_array);
    RUN_TEST(test_binary_search_single_element_found);
    RUN_TEST(test_binary_search_single_element_not_found);
    
    // 递归版本测试
    RUN_TEST(test_binary_search_recursive_found);
    RUN_TEST(test_binary_search_recursive_not_found);
    
    // 性能测试
    RUN_TEST(test_binary_search_large_array);
    
    return UNITY_END();
}
