#include "binary_search.h"

/**
 * 迭代版本的二分查找
 * @param arr 已排序的数组
 * @param size 数组大小
 * @param target 目标值
 * @return 目标值的索引，未找到返回-1
 */
int binary_search(int arr[], int size, int target) {
    int left = 0;
    int right = size - 1;
    
    while (left <= right) {
        // 防止整数溢出的中点计算
        int mid = left + (right - left) / 2;
        
        if (arr[mid] == target) {
            return mid;  // 找到目标值
        }
        else if (arr[mid] < target) {
            left = mid + 1;  // 在右半部分查找
        }
        else {
            right = mid - 1;  // 在左半部分查找
        }
    }
    
    return -1;  // 未找到
}

/**
 * 递归版本的二分查找
 * @param arr 已排序的数组
 * @param left 左边界
 * @param right 右边界
 * @param target 目标值
 * @return 目标值的索引，未找到返回-1
 */
int binary_search_recursive(int arr[], int left, int right, int target) {
    if (left > right) {
        return -1;  // 基本情况：未找到
    }
    
    int mid = left + (right - left) / 2;
    
    if (arr[mid] == target) {
        return mid;
    }
    else if (arr[mid] < target) {
        return binary_search_recursive(arr, mid + 1, right, target);
    }
    else {
        return binary_search_recursive(arr, left, mid - 1, target);
    }
}
