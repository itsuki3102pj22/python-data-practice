from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Hiragino Maru Gothis Pro", "Hiragino sans", "BIZ UDGothis", "MS Gothis"]

# ファイル読み込み
df = pd.read_csv(Path(__file__).with_name("test.csv"), index_col=0)

# データの可視化
# 折れ線グラフ
# df.plot()

# 棒グラフ
df.plot.bar()
plt.legend(loc="lower right")

# 棒グラフ（水平）
df.plot.barh()
plt.legend(loc="lower left")

# 積み上げ棒グラフ
df.plot.bar(stacked=True)
plt.legend(loc="lower right")

# 箱髭グラフ
df.plot.box()

# 面グラフ
df.plot.area()
plt.legend(loc="lower right")
plt.show()

# 円グラフ
df.loc["C子"].plot.pie(labels=df.columns, autopct='%1.1f%%')
plt.legend(loc="lower left")
plt.savefig("pie.png")

# 科目ごとの棒グラフ
df.T.plot.bar()
plt.legend(loc="lower right")
plt.show()