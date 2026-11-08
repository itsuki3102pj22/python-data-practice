import pandas as pd
from pathlib import Path

# ファイル読み込み
df = pd.read_csv(Path(__file__).with_name("sales_by_product.csv"), index_col=0)

# データ加工
# 売上金額追加
df["売上金額"] = df["単価"] * df["販売数"]

# 最後の行に合計金額追加
total_sales = df["売上金額"].sum()
df.loc["合計"] = ["", "", "", total_sales]
