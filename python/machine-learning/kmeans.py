import matplotlib.pyplot as plt
from rfm import get_rfm
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


def kmeans(df):
    show_elbow(df)


if __name__ == "__main__":
    df_user = get_rfm()

    kmeans(df_user)
