import pandas as pd
from pathlib import Path
import openpyxl

# ファイル読み込み
df = pd.read_csv(Path(__file__).with_name("test.csv"))

# ソート
kokugo = df.sort_values("国語", ascending=False)

# Excelファイル出力
with pd.ExcelWriter("csv_to_excel2.xlsx") as writer:
    df.to_excel(writer, index=False, sheet_name="元データ")
    kokugo.to_excel(writer, index=False, sheet_name="国語（ソート）")