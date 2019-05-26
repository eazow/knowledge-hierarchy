# -*- coding: utf-8 -*-

"""
九宫格解法：
2 9 4
7 5 3
6 1 8
"""


def judge_nine_nums(nums):
    nums.sort()

    if len(nums) != 9:
        return False

    result = nums[2-1] + nums[9-1] + nums[4-1] == nums[7-1] + nums[5-1] + nums[3-1] \
           == nums[6-1] + nums[1-1] + nums[8-1] == nums[2-1] + nums[5-1] + nums[8-1] \
           == nums[4-1] + nums[5-1] + nums[6-1] == nums[2-1] + nums[7-1] + nums[6-1] \
           == nums[9-1] + nums[5-1] + nums[1-1] == nums[4-1] + nums[3-1] + nums[8-1]
    if not result:
        print u"无解"

    return result


if __name__ == '__main__':
    assert judge_nine_nums(range(1, 10)) is True
    assert judge_nine_nums([5, 5, 6, 1, 2, 7, 9, 5, 8]) is False
