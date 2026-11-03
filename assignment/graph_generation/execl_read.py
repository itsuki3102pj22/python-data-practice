from openpyxl import load_workbook
from pathlib import Path

# openpyxlでExcelを操作
# Excelファイル読み込み
wb = load_workbook(Path(__file__).with_name("sales.xlsx"))
ws = wb.active

# A1セルの値を取得
print(ws["A1"].value)

# D1セルに売上金額を追加
ws["D1"] = "売上金額"

# 売上計算（単価*販売数）
for row in range(2, 7):
    tanka = ws[f"B{row}"].value
    hansok = ws[f"C{row}"].value

    ws[f"D{row}"] = tanka * hansok

# D7に合計金額入力
ws["D7"] = "=SUM(D2:D6)"

# 保存し再読み込み
output_path = Path(__file__).with_name("sales_updated.xlsx")
wb.save(output_path)

check_wb = load_workbook(output_path)
check_ws = check_wb.active

print(check_ws["D7"].value)
