def quick_sort_recursion(nums, left, right):
    if left >= right:
        return

    i, j, base_num = left, right, nums[left]

    while i < j:
        while i < j and nums[j] >= base_num:  # 从右向左寻找比base_num小的数
            j -= 1
        if j > i:
            nums[i] = nums[j]
            i += 1

        while i < j and nums[i] <= base_num:  # 从左向右寻找比base_num大的数
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
