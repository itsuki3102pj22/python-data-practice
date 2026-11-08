import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Hiragino Maru Gothis Pro", "Hiragino sans", "BIZ UDGothis", "MS Gothis"]
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.drawing.image import Image as XLImage

# ファイル一覧取得
data_dir = Path(__file__).parent/"data"
files = data_dir.glob("sales_*.csv")
# 売上目標データ
target_df = pd.read_csv(data_dir/"store_target.csv")
# データ出力先
data_dir_output = Path(__file__).parent/"output"



# csv読み込み
def load_sales_data(files):
    list_data = []
    for file in files:
        df = pd.read_csv(file)
        # 読み込んだデータをリストに追加
        list_data.append(df)
    
    # ベースデータ
    result_df = pd.concat(list_data, ignore_index=True)
    return result_df


# データ追加
def calculate_sales(df):
    df = df.copy()
    df["売上金額"] = df["単価"] * df["販売数"]
    return df


# グルーピング
def analyze_sales(base_df):
    # 店舗別売上
    groupby_branch = base_df.groupby("店舗名")[["販売数", "売上金額"]].sum()
    groupby_sorted_branch = groupby_branch.sort_values("売上金額", ascending=False)
    
    # 商品別売上
    groupby_products = base_df.groupby("商品名")[["販売数", "売上金額"]].sum()
    groupby_sorted_products = groupby_products.sort_values("売上金額", ascending=False)
    
    # 商品・店舗別売上
    groupby_branch_products = base_df.groupby(["商品名", "店舗名"])[["販売数", "売上金額"]].sum()

    return groupby_sorted_branch, groupby_sorted_products, groupby_branch_products


# 店舗別売上と売上目標を比較
def analyze_achievement(groupby_sorted_branch, target_df):
    # 店舗別売上と売上目標を結合
    merge_df = pd.merge(groupby_sorted_branch, target_df, on="店舗名", how="inner")
    # 目標差額を計算
    merge_df["目標差額"] = merge_df["売上金額"] - merge_df["売上目標"]
    # 達成率を計算し、小数２桁までに設定
    merge_df["達成率"] = merge_df["売上金額"] / merge_df["売上目標"] * 100
    merge_df["達成率"] = merge_df["達成率"].round(2)
    # 達成率の高い順にソート
    groupby_achievement = merge_df.sort_values("達成率", ascending=False)

    return groupby_achievement


# 日別売上の集計
def analyze_daily_sales(base_df):
    # 全店舗の日別売上
    daily_sales = base_df.groupby("日付")["売上金額"].sum().reset_index()
    #  店舗ごとの日別売上
    daily_branch_sales = base_df.groupby(["日付", "店舗名"])["売上金額"].sum().reset_index()

    # 店舗ごとの最高売上日
    max_sales_idx = daily_branch_sales.groupby("店舗名")["売上金額"].idxmax()
    branch_max_sales_day = daily_branch_sales.loc[max_sales_idx]
    branch_max_sales_day = branch_max_sales_day.sort_values("売上金額", ascending=False)

    return daily_sales, daily_branch_sales, branch_max_sales_day


# グラフ作成
def create_charts(daily_sales, daily_branch_sales, data_dir_output):
    # 全店舗日別売上の推移（折れ線グラフ）
    plt.figure(figsize=(10, 5))
    plt.plot(daily_sales["日付"], daily_sales["売上金額"])
    plt.title("全店舗の日別売上推移")
    plt.xlabel("日付")
    plt.ylabel("売上金額")
    plt.savefig(data_dir_output / "daily_sales.png", bbox_inches="tight") 
    plt.close()

    # 店舗別の日別売上比較（折れ線グラフ）
    plt.figure(figsize=(10, 5))
    pivot_df = daily_branch_sales.pivot_table(index="日付", columns="店舗名", values="売上金額")
    plt.plot(pivot_df.index, pivot_df["東京店"], label="東京店")
    plt.plot(pivot_df.index, pivot_df["大阪店"], label="大阪店")
    plt.plot(pivot_df.index, pivot_df["名古屋店"], label="名古屋店")
    plt.title("店舗別の日別売上比較")
    plt.xlabel("日付")
    plt.ylabel("売上金額")
    plt.legend()
    plt.savefig(data_dir_output / "daily_branch_sales.png", bbox_inches="tight")
    plt.close()


# Excelレポート出力
def export_excel(branch_achievement_df, groupby_sorted_products, daily_sales, branch_max_sales_day, output_path):
    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        # 店舗別実績
        branch_achievement_df.reset_index().to_excel(writer, sheet_name="店舗別実績", index=False)
    
        # 商品別実績
        groupby_sorted_products.reset_index().to_excel(writer, sheet_name="商品別実績", index=False)
    
        # 日別売上
        daily_sales.to_excel(writer, sheet_name="日別売上", index=False)
    
        # 最高売上日
        branch_max_sales_day.to_excel(writer, sheet_name="最高売上日", index=False)


# レポート加工
def format_excel(output_path, data_dir_output):
    wb = load_workbook(output_path)
    
    # ヘッダー設定
    header_fill = PatternFill(
        start_color="1F4E78", end_color="1F4E78", fill_type="solid"
    )
    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    header_alignment = Alignment(horizontal="center", vertical="center")
    
    sheet_names = ["店舗別実績", "商品別実績", "日別売上", "最高売上日"]
    target_columns = ["販売数", "売上金額", "売上目標", "目標差額"]
    
    for sheet_name in sheet_names:
        ws = wb[sheet_name]
        for cell in ws[1]:
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = header_alignment
    
        # 列幅調整
        for col in ws.columns:
            max_len = 0
    
            for cell in col:
                if cell.value is not None:
                    max_len = max(max_len, len(str(cell.value)))
    
            col_letter = col[0].column_letter
            ws.column_dimensions[col_letter].width = max(max_len + 4, 12)
    
        # 数字にカンマを追加
        header_map = {cell.value: cell.column for cell in ws[1]}
        for col_name in target_columns:
            if col_name in header_map:
                target_col = header_map[col_name]
    
                for row in ws.iter_rows(min_row=2):
                    cel = row[target_col - 1]
                    if cel.value is not None:
                        cel.number_format = '#,##0'
    
        # 達成率を％で表示
        if sheet_name == "店舗別実績":
            if "達成率" in header_map:
                target_col = header_map["達成率"]
    
                for row in ws.iter_rows(min_row=2):
                    cel = row[target_col - 1]
                    if cel.value is not None:
                        if cel.value > 1.0:
                            cel.value = cel.value / 100
    
                        cel.number_format = '0.00%'   
       
    # グラフ追加
    ws = wb["日別売上"]
    img = XLImage(data_dir_output/"daily_branch_sales.png")     
    img.width = 450
    img.height = 300
    
    img2 = XLImage(data_dir_output/"daily_sales.png")
    img2.width = 450
    img2.height = 300
    
    ws.add_image(img, "D1")
    ws.add_image(img2, "D17")
    # 保存
    wb.save(output_path)



# 実行手順
def main():
    # csvファイル読み込み
    result_df = load_sales_data(files)

    # 売上金額の計算
    base_df = calculate_sales(result_df)

    # 店舗別・商品別集計
    groupby_sorted_branch, groupby_sorted_products, groupby_branch_products = analyze_sales(base_df)

    # 目標達成率の分析
    branch_achievement_df = analyze_achievement(groupby_sorted_branch, target_df)

    # 日別売上の分析
    daily_sales, daily_branch_sales, branch_max_sales_day = analyze_daily_sales(base_df)

    # グラフ作成
    create_charts(daily_sales, daily_branch_sales, data_dir_output)

    # Excel出力
    output_path = data_dir_output/"sales_report.xlsx"
    export_excel(branch_achievement_df, groupby_sorted_products, daily_sales, branch_max_sales_day, output_path)

    # Excel加工
    format_excel(output_path, data_dir_output) 

if __name__ == "__main__":
    main()

