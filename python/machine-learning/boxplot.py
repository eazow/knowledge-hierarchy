import seaborn as sns
import pandas as pd

from utils import set_chinese_label


set_chinese_label()


df = pd.read_csv("data/wechat.csv")

data = pd.concat([df["浏览量"], df["热度指数"]], axis=1)  # 浏览量和热度指数
fig = sns.boxplot(x="热度指数", y="浏览量", data=data)  # 用seaborn的箱线图画图
fig.axis(ymin=0, ymax=800000)  # 设定y轴坐标
