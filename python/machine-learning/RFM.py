"""
RFM: Recency、Frequency、Monetary
"""

import pandas as pd
import matplotlib.pyplot as plt
from utils import set_chinese_label

set_chinese_label()

df = pd.read_csv("data/order.csv")

df = df.drop_duplicates()

print(df.describe())

df["消费日期"] = pd.to_datetime(df["消费日期"])

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
