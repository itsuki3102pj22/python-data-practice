import pandas as pd
from pathlib import Path

# ファイル読み込み
df = pd.read_csv(Path(__file__).with_name("test.csv"))

# 条件に合うデータ抽出
data_s = df[df["国語"] >= 90]
#print("国語の点数が90点以上\n", data_s)

data_c = df[df["数学"] < 70]
#print("数学の点数が70点未満\n", data_c)

# データ集計
# print(df[["名前", "数学"]])
# print("数学の最高点 : ", df["数学"].max())
# print("数学の最低点 : ", df["数学"].min())
# print("数学の平均点 : ", int(df["数学"].mean()))
# print("数学の中央値 : ", df["数学"].median())
# print("数学の合計点 : ", df["数学"].sum())

# データの並び替え
# print("国語の点数が高い順\n", df.sort_values("国語", ascending=False))

# 行と列の入れ替え
# print("行と列の入れ替え\n", df.T)

# データのリスト化
# print("データのリスト化\n", df.values)

#　CSVファイル出力
kokugo = df.sort_values("国語", ascending=False)
kokugo.to_csv("export.csv", index=False)


