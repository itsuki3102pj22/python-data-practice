import pandas as pd
from pathlib import Path

# 課題1：pandasでCSVを読み込み
# ファイル読み込み
df = pd.read_csv(Path(__file__).with_name("products.csv"))

# 商品名のみ出力
print("商品名\n", df["商品名"])
print("\n")

# 単価5,000円以上
data_s = df[df["単価"] >= 5000]
print("単価5,000円以上\n", data_s)
print("\n")

# 販売数10個以上
data_c = df[df["販売数"] >= 10]
print("販売数10個以上\n", data_c)
print("\n")

# データの行数、列数表示
print("行数 :", df.shape[0])
print("列数 :", df.shape[1])