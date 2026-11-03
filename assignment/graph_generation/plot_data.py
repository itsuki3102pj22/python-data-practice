from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Hiragino Maru Gothis Pro", "Hiragino sans", "BIZ UDGothis", "MS Gothis"]

# matplotlibでグラフ作成
# ファイル読み込み
df = pd.read_csv(Path(__file__).with_name("sales_result.csv"), index_col=0)

# 棒棒グラフ（X軸：商品名、Y軸：売上金額）
df["売上金額"].plot.bar()

plt.title("商品別売上金額")
plt.xlabel("商品名")
plt.ylabel("売上金額（円）")

# グラフ保存と表示
plt.savefig("sales_chart.png",  bbox_inches="tight") 
plt.show()

# 棒グラフ（X軸：商品名、Y軸：販売数）
plt.bar(df.index, df["販売数"])

plt.title("商品別販売数")
plt.xlabel("商品名")
plt.ylabel("販売数")

plt.savefig("sales_quantity.png", bbox_inches="tight")
plt.show()