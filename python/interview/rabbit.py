
def get_rabbits_count(step=4, month=10):
    """
    nums[i]=第i个月的兔子数
    nums[i-1]=第i-1个月的兔子数
    因为n[i-step]的兔子在第i个月必定成熟，会生出n[i-step]的兔子
    所以nums[i] = nums[i-step] + nums[i-1]
    :param step: 表示成熟所需的月数，即步长。假定题目中的4个月理解为4个月的月末
    :param month: 需计算兔子数的月数
    :return: 第month月的兔子数
    """
    nums = [1] * (month + 1)
    for i in range(step, month + 1):
        nums[i] = nums[i-step] + nums[i-1]

    return nums[month]


if __name__ == '__main__':
    assert get_rabbits_count(step=4, month=10) == 14
    assert get_rabbits_count(step=5, month=24) == 431
