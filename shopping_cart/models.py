# -*- coding:utf-8 -*-
from shopping_cart.settings import CATEGORIES
from shopping_cart.utils import TimeUtil


class ShoppingWebsite(object):
    """
    购物网站，维护网站的商品分类
    """
    def __init__(self):
        self.categories = CATEGORIES
        # 获取所有商品的分类
        self.product_category_map = self.get_product_category_map()

    def get_product_category_map(self):
        product_category_map = {}
        for category in self.categories:
            for product_name in self.categories.get(category):
                product_category_map[product_name] = category
        return product_category_map

    def get_product_category(self, product_name):
        return self.product_category_map.get(product_name)

    def settle(self, shopping_cart):
        """
        结算
        :param shopping_cart:
        :return:
        """
        total_price = 0
        for product, count in shopping_cart.products.items():
            category = product.category
            settle_date_discount = shopping_cart.discounts.get(shopping_cart.settle_date)
            category_discount = 1
            if settle_date_discount and category in settle_date_discount:
                category_discount = settle_date_discount.get(category)
            total_price += product.price * count * category_discount

        # 计算优惠券
        for coupon in shopping_cart.coupons:
            if shopping_cart.settle_timestamp <= coupon.expiry_timestamp and total_price > coupon.total_price:
                total_price -= coupon.discount_price
                # 只能用一张优惠券
                break

        return "%.2f" % total_price


class Product(object):
    """
    商品类
    """
    def __init__(self, name, price, category):
        self.name = name
        self.price = price
        self.category = category


class Coupon(object):
    def __init__(self, expiry_date, total_price, discount_price):
        self.expiry_date = expiry_date
        self.total_price = total_price
        self.discount_price = discount_price
        self.expiry_timestamp = TimeUtil.parse_date_to_timestamp(expiry_date)


class ShoppingCart(object):
    def __init__(self):
        self.products = {}
        self.discounts = {}
        self.coupons = []
        self.settle_date = None
        self.settle_timestamp = None

    def add_product(self, product, count):
        """
        添加商品
        :param product:
        :param count:
        :return:
        """
        if self.products.get(product) is None:
            self.products[product] = 0
        self.products[product] += count

    def add_coupon(self, coupon):
        """
        添加优惠券，并优惠金额从大到小
        :param coupon:
        :return:
        """
        self.coupons.append(coupon)
        # 将优惠券减免数额从大到小排序
        self.coupons.sort(lambda x, y: -cmp(x.discount_price, y.discount_price))

    def add_discount(self, date_str, category, discount_rate):
        """
        记录优惠信息
        :param date_str:
        :param category:
        :param discount_rate:
        :return:
        """
        if self.discounts.get(date_str) is None:
            self.discounts[date_str] = {}
        self.discounts[date_str][category] = discount_rate
