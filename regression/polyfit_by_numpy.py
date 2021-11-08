import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import sympy as sym
from sympy.plotting import plot

df = pd.read_csv("docvocabsize.csv")

x_observed= df["doc_size"].values.tolist()
y_observed= df["vocab_size"].values.tolist()

x_latent = np.linspace(min(x_observed), max(x_observed), 100)
cf2 = ["最小2乗法（2次式）", lambda x, y: np.polyfit(x_observed, y_observed, 2)]

sym.init_printing(use_unicode=True)

x, y = sym.symbols("x y")

for method_name, method in [cf2]:
    print(method_name)
    # 係数の計算
    coefficients = method(x_observed, y_observed)

    # Sympy を用いた数式の表示
    expr = 0
    for index, coefficient in enumerate(coefficients):
        expr += coefficient * x ** (len(coefficients) - index - 1)
    # display(sym.Eq(y, expr))

    # プロットと曲線の表示
    fitted_curve = np.poly1d(method(x_observed, y_observed))(x_latent)
    plt.scatter(x_observed, y_observed, label="observed")
    plt.plot(x_latent, fitted_curve, c="red", label="fitted")
    plt.grid()
    plt.legend()
    # plt.show()
    plt.savefig("matplotlib.png")