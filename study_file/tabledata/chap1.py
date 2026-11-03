from pathlib import Path

import pandas as pd

# ファイル読み込み
df = pd.read_csv(Path(__file__).with_name("test.csv"))

#print("国語と数学の列データ\n", df[["国語", "数学"]])
#print("C子のデータ\n", df.loc[2])
#print("C子の数学の点数 :", df.loc[2, "数学"])

# 1列追加
df["美術"] = [80, 90, 70, 65, 85, 75]
#print("美術のデータ\n", df["美術"])

# 1行追加
df.loc[6] = ["F子", 90, 92, 96, 97, 88, 91]
#print("F子のデータ\n", df.loc[6]) 

# 1列削除
print("美術を削除\n", df.drop("美術", axis=1))

# 1行削除
print("F子を削除\n", df.drop(6, axis=0))