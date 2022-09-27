import matplotlib.pyplot as plt
import pandas as pd

from utils import set_chinese_label


set_chinese_label()


df = pd.read_csv("data/wechat.csv")

plt.plot(df["点赞数"], df["浏览量"], "r.", label="Training data")
plt.xlabel("点赞数")
plt.ylabel("浏览量")
plt.legend()
plt.show()
