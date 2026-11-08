import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Hiragino Maru Gothis Pro", "Hiragino sans", "BIZ UDGothis", "MS Gothis"]
from openpyxl import Workbook
from openpyxl.drawing.image import Image


# ファイル読み込み
df = pd.read_csv(Path(__file__).with_name("products.csv"))

# データ加工
# 売上金額の列追加
df["売上金額"] = df["単価"] * df["販売数"]

# 商品別にグルーピングし、売上金額順にソート
groupby_df = df.groupby("商品名")[["販売数", "売上金額"]].sum()
groupby_sorted_sales = groupby_df.sort_values("売上金額", ascending=False)
groupby_sorted_quantity = groupby_df.sort_values("販売数", ascending=False)

# 売上金額を棒グラフで表示(タイトル：商品別売上金額、X軸：商品名、Y軸：売上金額)
groupby_sorted_sales["売上金額"].plot.bar()
plt.title("商品別売上金額")
plt.xlabel("商品名")
plt.ylabel("売上金額")

plt.savefig("sales_chart.png", bbox_inches="tight")
plt.show()
plt.close()

# 商品別販売数を棒グラフで表示(タイトル：商品別販売数、X軸：商品名、Y軸：販売数)
groupby_sorted_quantity["販売数"].plot.bar()
plt.title("商品別販売数")
plt.xlabel("商品名")
plt.ylabel("販売数")

plt.savefig("sales_quantity.png", bbox_inches="tight")
plt.show()
plt.close()

# Excelファイル作成
wb = Workbook()
ws = wb.active
ws.title = "商品別集計データ"

# 列名追加
ws["A1"] = "商品名"
ws["B1"] = "販売数"
ws["C1"] = "売上金額"

row_num = 2

for index, row in groupby_sorted_sales.iterrows():
    ws[f"A{row_num}"] = index
    ws[f"B{row_num}"] = row["販売数"]
    ws[f"C{row_num}"] = row["売上金額"]

    row_num += 1

ws[f"A{row_num}"] = "合計"
ws[f"B{row_num}"] = f"=SUM(B2:B{row_num -1})"
ws[f"C{row_num}"] = f"=SUM(C2:C{row_num -1})"

# グラフ挿入
img = Image("sales_chart.png")
img2 = Image("sales_quantity.png")
ws.add_image(img, "E2")
ws.add_image(img2, "E20")

# ファイル保存
output_path = Path(__file__).with_name("monthly_sales_report.xlsx")
wb.save(output_path)