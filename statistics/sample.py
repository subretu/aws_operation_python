import numpy as np

# CSVのロード
data = np.genfromtxt("data.csv", delimiter=",", skip_header=1, dtype="float")
# 対象の列を抽出
y = data[:, 2]
# xの値をyから生成
x = np.linspace(1, len(y), len(y))
# フィッティング
a, b = np.polyfit(x, y, 1)
