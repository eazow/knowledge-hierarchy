"""
RFM: Recency、Frequency、Monetary
"""

import pandas as pd
import matplotlib.pyplot as plt
from utils import set_chinese_label

set_chinese_label()


def clean(df):
    df = df.drop_duplicates()

    df = df.loc[df["数量"] > 0]
    print(df.describe())
    return df


def get_rfm():
    df = pd.read_csv("data/order.csv")

    clean(df)

    df["消费日期"] = pd.to_datetime(df["消费日期"])
    df["总价"] = df["单价"] * df["数量"]

    # draw_monthly_orders_plot(df)

    df_user = get_df_user(df)
    df_user = get_recency(df, df_user)
    df_user = get_frequency(df, df_user)
    return get_monetary(df, df_user)


def draw_monthly_orders_plot(df):
    df_orders_monthly = df.set_index("消费日期")["订单号"].resample("M").nunique()  # 每个月的订单数量

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


def get_df_user(df):
    df_user = pd.DataFrame(df["用户码"].unique())
    df_user.columns = ["用户码"]
    return df_user.sort_values(by="用户码", ascending=True).reset_index(drop=True)


def get_recency(df, df_user):
    df_recent_buy = df.groupby("用户码").消费日期.max().reset_index()  # 构建消费日期信息
    df_recent_buy.columns = ["用户码", "最近日期"]
    df_recent_buy["R值"] = (
        df_recent_buy["最近日期"].max() - df_recent_buy["最近日期"]
    ).dt.days  # 计算最新日期与上次消费日期的天数
    return pd.merge(df_user, df_recent_buy[["用户码", "R值"]], on="用户码")


def get_frequency(df, df_user):
    df_frequency = df.groupby("用户码").消费日期.count().reset_index()
    df_frequency.columns = ["用户码", "F值"]  # 设定字段名称
    return pd.merge(df_user, df_frequency, on="用户码")


def get_monetary(df, df_user):
    df_revenue = df.groupby("用户码").总价.sum().reset_index()  # 根据消费总额，构建df_revenue对象
    df_revenue.columns = ["用户码", "M值"]  # 设定字段名称
    return pd.merge(df_user, df_revenue, on="用户码")  # 把消费金额整合至df_user结构


def draw_histogram(df):
    df_user["R值"].plot(kind="hist", bins=20, title="新进度分布直方图").show()  # R值直方图

    df_user.query("F值 < 800")["F值"].plot(
        kind="hist", bins=50, title="消费频率分布直方图"
    )  # F值直方图

    df_user.query("M值 < 20000")["M值"].plot(
        kind="hist", bins=50, title="消费金额分布直方图"
    )  # M值直方图


def kmeans(df):
    from sklearn.cluster import KMeans  # 导入KMeans模块

    def show_elbow(df):  # 定义手肘函数
        distance_list = []  # 聚质心的距离（损失）
        K = range(1, 9)  # K值范围
        for k in K:
            kmeans = KMeans(n_clusters=k, max_iter=100)  # 创建KMeans模型
            kmeans = kmeans.fit(df)  # 拟合模型
            distance_list.append(kmeans.inertia_)  # 创建每个K值的损失
        plt.plot(K, distance_list, "bx-")  # 绘图
        plt.xlabel("k")
        plt.ylabel("距离均方误差")
        plt.title("k值手肘图")

    show_elbow(df)


if __name__ == "__main__":
    df_user = get_rfm()

    draw_histogram(df_user)

    kmeans(df_user)
