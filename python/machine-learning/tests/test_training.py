import pandas as pd
import pytest
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression


@pytest.mark.parametrize("fit_intercept", [True, False])
@pytest.mark.parametrize("normalize", [True, False])
def test_linear_regression(fit_intercept, normalize):
    df = pd.read_csv("../data/wechat.csv").dropna()

    x = df.drop(["浏览量"], axis=1)  # feature set
    y = df.浏览量  # label set

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=0
    )

    linear_regression_model = LinearRegression(fit_intercept=fit_intercept, normalize=normalize)  # 使用线性回归算法创建模型

    linear_regression_model.fit(x_train, y_train)  # 用训练集数据，训练机器，拟合函数，确定内部参数

    y_predict = linear_regression_model.predict(x_test)  # 预测测试集的Y值

    df_predict = x_test.copy()  # 测试集特征数据
    df_predict["浏览量真值"] = y_test  # 测试集标签真值
    df_predict["浏览量预测值"] = y_predict  # 测试集标签预测值
    print(df_predict)

    print("当前模型的4个特征的权重分别是: ", linear_regression_model.coef_)
    print("当前模型的截距（偏置）是: ", linear_regression_model.intercept_)
    print("线性回归预测评分：", linear_regression_model.score(x_test, y_test))  # 评估模型
