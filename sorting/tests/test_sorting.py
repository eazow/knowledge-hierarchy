from sorting.quick_sort import quick_sort
from sorting.selection_sort import selection_sort


def test_quick_sort():
    nums = [10, 30, 5, 1, 100, 20, 6, 50]
    assert quick_sort(nums) == [1, 5, 6, 10, 20, 30, 50, 100]


def test_selection_sort():
    nums = [10, 30, 5, 1, 100, 20, 6, 50]
    assert selection_sort(nums) == [1, 5, 6, 10, 20, 30, 50, 100]
