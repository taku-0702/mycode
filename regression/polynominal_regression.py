from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

import glob

class Regression:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def plot(self, fig_file_name: str):
        pred = self.model1.predict(self.X)

        plt.scatter(self.x, self.y, c="blue", alpha=0.3)
        plt.plot(self.x, pred, c="red")

        plt.savefig(f"{fig_file_name}.png")

    def regression(self, degree):
        np.random.seed(123)

        self.X = self.x.reshape(-1, 1)

        _x = PolynomialFeatures(degree=degree)

        self.model1 = LinearRegression()
        self.X = _x.fit_transform(self.X)
        self.model1.fit(self.X, self.y)

        # print("切片: ", self.model1.intercept_)
        # print("傾き", self.model1.coef_)

        return self.model1.intercept_, self.model1.coef_

if __name__ == "__main__":
    target_files = glob.glob("train/*.csv")
    degree = 2

    intercept_lst = []
    coefficient_lst = []

    for target_file in target_files:
        df = pd.read_csv(target_file, header=0)

        x = df["word_num"].apply(math.log).values
        y = (df["vocab_size"] / df["word_num"]).apply(math.log).values

        regression = Regression(x, y)
        intercept, coefficient = regression.regression(degree=degree)
        # print(intercept, type(coefficient))
        intercept_lst.append(intercept)
        coefficient_lst.append(coefficient)

    coefficient_array = np.array(coefficient_lst)
    print(coefficient_array)
    print(sum(intercept_lst) / len(intercept_lst))
    print(np.mean(coefficient_array, axis=0))
