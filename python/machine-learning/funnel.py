import plotly.express as px

data = dict( 
    number=[59, 32, 18, 9, 2], 
    stage=["访问数", "下载数", "注册数", "搜索数", "付款数"]
)
fig = px.funnel(data, x='number', y='stage')
fig.show()
