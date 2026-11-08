import pandas as pd
from pathlib import Path

# 課題2：pandasでデータを加工
#　ファイル読み込み
df = pd.read_csv(Path(__file__).with_name("products.csv"))

# 売上金額の列追加
df["売上金額"] = df["単価"] * df["販売数"]

# 商品別にグルーピング
groupby_df = df.groupby("商品名")[["販売数", "売上金額"]].sum()
print("商品別にグルーピング\n", groupby_df)

# 売上金額の高い順にソート
sales_sorted = groupby_df.sort_values("売上金額", ascending=False)
print("売上金額の高い順\n", sales_sorted)

# # 販売数の平均
# average_sales = df["販売数"].mean()
# print("販売数の平均 :", average_sales)

# # 売上金額10万以上を抽出
# high_sales = df[df["売上金額"] >= 100000]
# print("売上金額10万以上\n", high_sales)

# 売上金額追加後のデータをcsvファイルに出力
output_path = Path(__file__).with_name("sales_summary.csv")
sales_sorted.to_csv(output_path)