### 购物车

#### 说明
1. main函数在shopping.py中
2. tests目录包含一些合法、非法输入的测试用例
3. settings.py为配置文件
4. utils.py为工具类，比如包含日期处理、异常处理
5. models.py为模型层，包含购物车、购物网站、优惠券、商品的定义
6. 将输入的字符串解析并计算金额的过程看作是用户进购物网站选购，获取优惠信息，优惠券，将商品加入购物车，以及最后结算的过程；将程序和现实世界对应了起来，符合面向对象设计原则，并能很好的理解代码逻辑
7. 入口代码，可以理解为顾客根据购物信息(shopping_info)购物(shopping)并且结算(settle)
```
Customer().shopping_and_settle(shopping_info)
```
