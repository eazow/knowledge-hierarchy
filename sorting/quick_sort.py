# -*- coding:utf-8 -*-


def quick_sort_recursion(nums, left, right):
    if left >= right:
        return

    i = left
    j = right
    base_num = nums[left]

    while i < j:
        # 从右向左寻找比base_num小的数
        while i < j and nums[j] >= base_num:
            j -= 1
        if j > i:
            nums[i] = nums[j]
            i += 1
        # 从左向右寻找比base_num大的数
        while i < j and nums[i] <= base_num:
            i += 1
        if i < j:
            nums[j] = nums[i]
            j -= 1

    nums[i] = base_num

    quick_sort_recursion(nums, left, i - 1)
    quick_sort_recursion(nums, i + 1, right)


def quick_sort(nums):
    quick_sort_recursion(nums, 0, len(nums) - 1)
    return nums


if __name__ == "__main__":
    the_nums = [10, 30, 5, 1, 100, 20, 6, 50]
    assert quick_sort(the_nums) == [1, 5, 6, 10, 20, 30, 50, 100]
