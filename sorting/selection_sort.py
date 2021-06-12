def selection_sort(nums):
    for i in range(len(nums)):
        min_index = i
        for j in range(i + 1, len(nums)):
            if nums[j] < nums[min_index]:
                nums[min_index], nums[j] = nums[j], nums[min_index]

    return nums


if __name__ == "__main__":
    nums = [10, 30, 5, 1, 100, 20, 6, 50]
    assert selection_sort(nums) == [1, 5, 6, 10, 20, 30, 50, 100]
