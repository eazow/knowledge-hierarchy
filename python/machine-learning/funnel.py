import plotly.express as px
import pandas as pd


stages = ["访问数", "下载数", "注册数", "搜索数", "付款数"]
data = dict(number=[59, 32, 18, 9, 2], stage=stages)
px.funnel(data, x="number", y="stage").show()


df_male = pd.DataFrame(dict(number=[59, 32, 18, 9, 2], stage=stages, gender=["男"] * 5))
df_female = pd.DataFrame(dict(number=[29, 17, 8, 3, 1], stage=stages, gender=["女"] * 5))
px.funnel(pd.concat([df_male, df_female]), x="number", y="stage", color="gender").show()
