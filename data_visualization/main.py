import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math 

df = pd.read_csv("docvocabsize.csv")

# 台紙figureを初期化
fig = plt.figure()

# figureとaxesを同時に初期化
# fig, ax = plt.subplots()

ax1 = fig.add_subplot(2, 1, 1)
ax2 = fig.add_subplot(2, 1, 2)
# ax3 = fig.add_subplot(2, 2, 3)
# ax4 = fig.add_subplot(2, 2, 4)

p = np.log(np.linspace(1, 1500000, 1000000))   # linspace(min, max, N) で範囲 min から max を N 分割します
q = 0.00726895*(p**2) + -0.19805659*p + 1.3585838055892019

ax1.plot(p, q)
ax1.plot(df["doc_size"].apply(math.log), df["vocab_size"] / df["doc_size"])

# plt.show()
plt.savefig("matplotlib.png")
