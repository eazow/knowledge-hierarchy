"""
RFM: Recency、Frequency、Monetary
"""

import pandas as pd
import matplotlib.pyplot as plt
from utils import set_chinese_label

set_chinese_label()

df = pd.read_csv("data/order.csv")

df = df.drop_duplicates()

df = df.loc[df["数量"] > 0]
print(df.describe())

df["消费日期"] = pd.to_datetime(df["消费日期"])
df["总价"] = df["单价"] * df["数量"]

print(df.set_index("消费日期")["订单号"].resample("M").nunique())
df_orders_monthly = df.set_index("消费日期")["订单号"].resample("M").nunique()  # 每个月的订单数量

print(df_orders_monthly.values)

ax = pd.DataFrame(df_orders_monthly.values).plot(
    grid=True, figsize=(12, 6), legend=False
)
ax.set_xlabel("月份")
ax.set_ylabel("订单数")
ax.set_title("月度订单数")
plt.xticks(
    range(len(df_orders_monthly.index)),
    [x.strftime("%Y.%m") for x in df_orders_monthly.index],
    rotation=45,
)
plt.show()


df_user = pd.DataFrame(df["用户码"].unique())  # 生成以用户码为主键的结构df_user
df_user.columns = ["用户码"]
df_user = df_user.sort_values(by="用户码", ascending=True).reset_index(drop=True)
print(df_user)


df_recent_buy = df.groupby("用户码").消费日期.max().reset_index()  # 构建消费日期信息
df_recent_buy.columns = ["用户码", "最近日期"]
df_recent_buy["R值"] = (
    df_recent_buy["最近日期"].max() - df_recent_buy["最近日期"]
).dt.days  # 计算最新日期与上次消费日期的天数
df_user = pd.merge(
    df_user, df_recent_buy[["用户码", "R值"]], on="用户码"
)  # 把上次消费距最新日期的天数（R值）合并至df_user结构
print(df_user.head())  # 显示df_user头几行数据
