import os

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

from utils import set_chinese_label

dirpath = os.path.dirname(__file__)

set_chinese_label()

df = pd.read_csv(os.path.join(dirpath, "data/wechat.csv"))

print(df.isna())

plt.plot(
    df["点赞数"], df["浏览量"], "r.", label="Training data"
)  # 用matplotlib.pyplot的plot方法显示散点图
plt.xlabel("点赞数")  # x轴Label
plt.ylabel("浏览量")  # y轴Label
plt.legend()  # 显示图例
plt.show()  # 显示绘图结果


fig = sns.boxplot(x="热度指数", y="浏览量", data=df[["浏览量", "热度指数"]])  # 用seaborn的箱线图画图
fig.axis(ymin=0, ymax=800000)  # 设定y轴坐标


pd.concat([df["点赞数"], df["浏览量"]])
