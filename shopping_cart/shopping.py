# -*- coding:utf-8 -*-

import re
from shopping_cart.models import Product, ShoppingWebsite, Coupon, ShoppingCart
from shopping_cart.settings import REGEX
from shopping_cart.utils import TimeUtil, exception_handler


class Customer(object):
    """
    顾客类
    """
    def __init__(self):
        self.shopping_website = ShoppingWebsite()
        self.shopping_cart = ShoppingCart()

    @exception_handler
    def shopping_and_settle(self, shopping_info):
        """
        顾客购物和结算
        :param shopping_info:
        :return:
        """
        self.shopping(shopping_info)
        return self.shopping_website.settle(self.shopping_cart)

    def shopping(self, shopping_info):
        """
        顾客购物，即将商品装入购物车, 以及处理折扣、优惠券信息
        :param shopping_info:
        :return: 
        """
        for line in shopping_info.splitlines():
            line = line.strip()
            if len(line) == 0:
                continue

            # 获取折扣信息
            if self.get_discount(line):
                continue

            # 获取商品信息
            if self.get_product(line):
                continue

            # 获取优惠券
            if self.get_coupon(line):
                continue

            # 获取结账日期，如果不为结账日期，则表明该行输入数据有问题
            if not self.get_date(line):
                raise Exception("Wrong line: %s" % line)

    def get_discount(self, line):
        """
        获取折扣信息
        2013.11.11 | 0.7 | 电子
        :param line: re match对象
        :return:
        """
        discount_match = re.match(REGEX.DISCOUNT_LINE, line)
        if discount_match:
            date_str = discount_match.group(1)
            discount_rate = float(discount_match.group(2))
            category = discount_match.group(3)
            if category not in self.shopping_website.categories:
                raise Exception("Wrong category")

            self.shopping_cart.add_discount(date_str, category, discount_rate)

        return discount_match is not None

    def get_product(self, line):
        """
        获取商品信息
        :param line: 1 * 显示器: 1799.00
                     12 * 啤酒: 25.00
                     5 * 面包: 9.00
        :return:
        """
        product_match = re.match(REGEX.PRODUCT_LINE, line)
        if product_match:
            count = int(product_match.group(1))
            product_name = product_match.group(2)
            price = float(product_match.group(3))
            category = self.shopping_website.get_product_category(product_name)
            if category is None:
                raise Exception("Wrong product name")

            self.shopping_cart.add_product(Product(product_name, price, category), count)

        return product_match is not None

    def get_coupon(self, line):
        """
        获取优惠券
        :param line: 2014.3.2 | 1000 | 200
        :return:
        """
        coupon_match = re.match(REGEX.COUPON_LINE, line)
        if coupon_match:
            expiry_date = coupon_match.group(1)
            coupon_total_price = float(coupon_match.group(2))
            coupon_discount_price = float(coupon_match.group(3))

            self.shopping_cart.add_coupon(Coupon(expiry_date, coupon_total_price, coupon_discount_price))

        return coupon_match is not None

    def get_date(self, line):
        date_match = re.match(REGEX.DATE_ONLY, line)
        if date_match:
            settle_date = date_match.group()
            self.shopping_cart.settle_date = settle_date
            self.shopping_cart.settle_timestamp = TimeUtil.parse_date_to_timestamp(settle_date)

        return date_match is not None


if __name__ == "__main__":
    shopping_info1 = u"""\
2013.11.11 | 0.7 | 电子

1 * iPad: 2399.00
1 * 显示器: 1799.00
12 * 啤酒: 25.00
5 * 面包: 9.00

2013.11.11
2014.5.1 | 500 | 100
2014.3.2 | 1000 | 200
"""
    total_price = Customer().shopping_and_settle(shopping_info1)
    assert total_price == "3083.60"

    shopping_info2 = u"""\
2019.6.14 | 0.7 | 电子
2019.6.14 | 0.8 | 日用品
2019.6.18 | 0.1 | 食品

1 * iPad: 1000.00
12 * 啤酒: 10.00
8 * 餐巾纸: 1.00
3 * 蔬菜: 10.00
                
2019.6.14
"""
    total_price = Customer().shopping_and_settle(shopping_info2)
    assert total_price == "856.40"

