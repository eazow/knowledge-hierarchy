import pandas as pd
from sklearn.model_selection import train_test_split

df = pd.read_csv("data/wechat.csv").dropna()

x = df.drop(["浏览量"], axis=1)  # feature set

y = df.浏览量  # label set

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)
