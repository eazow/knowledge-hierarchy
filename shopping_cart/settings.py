# -*- coding:utf-8 -*-


class REGEX(object):
    DISCOUNT = "0\.\d"
    DATE = "\d{4}.\d{1,2}.\d{1,2}"
    CHINESE = ".{2,3}"
    NUMBER = "\d{1,10}"

    DISCOUNT_LINE = r"(%s) \| (%s) \| (%s)" % (DATE, DISCOUNT, CHINESE)
    PRODUCT_LINE = r"(\d+) \* (.{1,5}): (\d+.\d{2})"
    COUPON_LINE = r"(%s) \| (%s) \| (%s)" % (DATE, NUMBER, NUMBER)

# 商品所有分类
CATEGORIES = {
    u"电子": ["iPad", "iPhone", u"显示器", u"笔记本电脑", u"键盘"],
    u"食品": [u"面包", u"饼干", u"蛋糕", u"牛肉", u"鱼", u"蔬菜"],
    u"日用品": [u"餐巾纸", u"收纳箱", u"咖啡杯", u"雨伞"],
    u"酒类": [u"啤酒", u"白酒", u"伏特加"]
}


# class STATE(object):
#     START = 0
#     DISCOUNT = 1
#     PRODUCT = 2
#     DATE = 3
#     COUPON = 4