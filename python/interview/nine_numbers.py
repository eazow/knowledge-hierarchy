"""
时间复杂度O(1)
空间复杂度O(1)

九宫格的一种解法：
2 9 4
7 5 3
6 1 8
其中2可以理解为索引，即第2个数，对应到nums中为nums[2-1]
每一行、每一列、以及对角线的和相同
比如第1、2行的和相同，即第2个、第9个、第4个数的和要 == 第7个、第5个、第3个数的和
"""


def judge_nine_nums(nums):
    nums.sort()

    if len(nums) != 9:
        return False

    result = (
        nums[2 - 1] + nums[9 - 1] + nums[4 - 1]
        == nums[7 - 1] + nums[5 - 1] + nums[3 - 1]
        == nums[6 - 1] + nums[1 - 1] + nums[8 - 1]
        == nums[2 - 1] + nums[5 - 1] + nums[8 - 1]
        == nums[4 - 1] + nums[5 - 1] + nums[6 - 1]
        == nums[2 - 1] + nums[7 - 1] + nums[6 - 1]
        == nums[9 - 1] + nums[5 - 1] + nums[1 - 1]
        == nums[4 - 1] + nums[3 - 1] + nums[8 - 1]
    )
    if not result:
        print("无解")

    return result


if __name__ == "__main__":
    assert judge_nine_nums(range(1, 10)) is True
    assert judge_nine_nums([5, 5, 6, 1, 2, 7, 9, 5, 8]) is False
