import sqlite3
from pathlib import Path
import pandas as pd
import shutil

# パス指定
data_dir = Path(__file__).parent / "data"
files = data_dir.glob("sales_*.csv")
main_db = Path(__file__).parent / "sales.db"
backup_db = Path(__file__).parent / "sales_backup.db"
output_file = Path(__file__).parent / "output"

# 追加データ
sales_data = [
    ("2026-10-01", "東京店", "PC", 120000, 5),
    ("2026-10-02", "東京店", "マウス", 3000, 12),
]


# CSV読み込み
def read_csv(files):
    list_data = []

    for file in files:
        df = pd.read_csv(file)
        list_data.append(df)
        print(f"{file.name}から{len(df)}件取得しました。")

    result_df = pd.concat(list_data, ignore_index=True)
    print(f"合計{len(result_df)}件のデータを取得しました。")
    return result_df


# 読み込んだデータを登録できる状態へ
def list_read_csv(sales_data):
    upsert_list = []

    # SQLiteへの登録に向けてデータ型を調整
    clean_df = sales_data.astype(object)

    for _, row in clean_df.iterrows():
        upsert_list.append(row.tolist())
    return upsert_list


# DBへ接続
def connect_db(main_db):
    connection = sqlite3.connect(main_db)
    print("データベース「sales.db」へ接続しました。")
    return connection


# DB接続解除
def close_db(connection):
    connection.close()
    print("接続を閉じました。")


# CREATE
# ①salesテーブル
def create_sales(connection):
    connection.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            "日付" TEXT,
            "店舗名" TEXT,
            "商品名" TEXT,
            "単価" INTEGER,
            "販売数" INTEGER,
            UNIQUE ("日付", "店舗名", "商品名")
        ) 
        """)
    connection.commit()
    print("salesテーブルを作成しました。")
    return connection


# DROP
# salesテーブル削除
def delete_sales(connection):
    connection.execute("DROP TABLE IF EXISTS sales;")
    connection.commit()
    print("テーブルを削除しました。")


# INSERT
# salesテーブルデータ追加
def insert_sales(connection, insert_list):
    total_csv_count = len(insert_list)

    before_changes = connection.total_changes

    connection.executemany(
        """
        INSERT OR IGNORE INTO sales ("日付", "店舗名", "商品名", "単価", "販売数")
        VALUES (?, ?, ?, ?, ?);
        """,
        insert_list,
    )
    connection.commit()

    inserted_count = connection.total_changes - before_changes
    skipped_count = total_csv_count - inserted_count

    print(f"csv読み込み件数: {total_csv_count}件")
    print(f"新規登録件数: {inserted_count}件")
    print(f"未登録（重複スキップ）件数: {skipped_count}件")


# UPSERT
# salesテーブル追加・更新
def upsert_sales(connection, upsert_list):
    connection.executemany(
        """
        INSERT INTO sales ("日付", "店舗名", "商品名", "単価", "販売数")
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT ("日付", "店舗名", "商品名")
        DO UPDATE SET
            "単価" = excluded."単価",
            "販売数" = excluded."販売数";
            """,
        upsert_list,
    )
    connection.commit()
    print(f"UPSERT処理対象：{len(upsert_list)}件")


# SELECT
# テーブルの存在確認
def check_sales_table(connection):
    check_table = connection.execute("""
    SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'sales';
    """)
    name = check_table.fetchall()
    if name:
        print(f"{name}は存在しています。")
    else:
        print("テーブルは存在していません。")


# 件数確認（sales)
def count_sales(connection):
    count_sales = connection.execute("SELECT COUNT(*) FROM sales;")
    count = count_sales.fetchone()[0]
    print(f"{count}件取得")


# salesテーブルのデータ確認
def check_select_sales(connection):
    check_data = connection.execute("""SELECT * FROM sales WHERE
    "店舗名" = '東京店' AND "商品名" IN ('PC', 'マウス');
    """)
    data = check_data.fetchall()
    print(data)


# グルーピング
def summary_sales(connection):
    group = connection.execute(
        """SELECT "店舗名", SUM("販売数") FROM sales GROUP BY "店舗名";"""
    )
    group_branch = group.fetchall()
    print(group_branch)


# 商品ごとの売上金額
def summary_product_revenue(connection):
    total = connection.execute("""SELECT "商品名", SUM("単価" * "販売数") AS "売上金額"
    FROM sales GROUP BY "商品名" ORDER BY "売上金額" DESC;""")
    total_products = total.fetchall()
    print(total_products)


# 店舗*商品別売上集計
def summary_store_product(connection):
    total = connection.execute(
        """SELECT "店舗名", "商品名", SUM("単価" * "販売数") AS "売上金額"
    FROM sales GROUP BY "店舗名", "商品名" ORDER BY "店舗名" ASC, "売上金額" DESC;"""
    )
    total_amount = total.fetchall()
    print(total_amount)


# 店舗別売上 450,000以上
def summary_high_revenue(connection):
    total = connection.execute(
        """SELECT "店舗名", SUM("単価" * "販売数") AS "売上金額"
        FROM sales GROUP BY "店舗名" HAVING "売上金額" >= 450000 ORDER BY "売上金額" DESC;"""
    )
    total_store = total.fetchall()
    print(total_store)


# 店舗別売上（PC除く）
def summary_without_pc(connection):
    total = connection.execute(
        """SELECT "店舗名", SUM("単価" * "販売数") AS "売上金額"
        FROM sales WHERE "商品名" != "PC" GROUP BY "店舗名" HAVING SUM("単価" * "販売数") >= 150000 ORDER BY "売上金額" DESC"""
    )
    total_store = total.fetchall()
    print(total_store)


# 全店舗の売上
def summary_all_sales(connection):
    total = connection.execute(
        """SELECT SUM("単価" * "販売数") AS "売上金額" FROM sales;"""
    )
    total_sales = total.fetchone()
    return total_sales[0] if total_sales and total_sales[0] else 0


# 店舗別売上
def summary_revenue(connection):
    total = connection.execute("""SELECT "店舗名", SUM("単価" * "販売数") AS "売上金額"
    FROM sales GROUP BY "店舗名" ORDER BY "売上金額" DESC;""")
    store_sales = total.fetchall()
    return store_sales


# 売上構成比
def summary_total_rate(total_store, store_sales):
    store_rate = []

    if total_store == 0:
        return store_rate

    for store, revenue in store_sales:
        rate = (revenue / total_store) * 100
        store_rate.append((store, round(rate, 1)))
    return store_rate


# pandas読み取り用
def sql_to_dataframe(connection):
    sql = """SELECT "店舗名", SUM("単価" * "販売数") AS "売上金額" 
      FROM sales GROUP BY "店舗名" ORDER BY "売上金額" DESC;"""

    df = pd.read_sql_query(sql, connection)
    output_file.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_file / "store_revenue.csv", index=False)


df1 = pd.DataFrame(
    {"店舗名": ["東京店", "大阪店", "名古屋店"], "売上比率": [29.9, 35.0, 35.1]}
)
df2 = pd.DataFrame(
    {
        "店舗名": ["東京 店", "大阪　店", "名古屋 店"],
        "売上金額": [415000, 486500, 488500],
    }
)
df3 = pd.DataFrame(
        {
            "店舗名": ["東京店", "大阪店", "名古屋店", "東京店"],
            "売上金額": [415000, 486500, 488500, 415000],
        }
    )
df4 = pd.DataFrame({
    "店舗名": ["東京店", "東京店", "東京店", "大阪店", "大阪店"],
    "日付": [
        "2026-11-01",
        "2026-11-01",
        "2026-11-02",
        "2026-11-01",
        "2026-11-02"
    ],
    "売上金額": [100000, 100000, 100000, 80000, 80000]
})
df5 = pd.DataFrame({
    "店舗名": ["東京店", "東京店", "東京店", "大阪店", "大阪店"],
    "日付": [
        "2026-11-01",
        "2026-11-01",
        "2026-11-02",
        "2026-11-01",
        "2026-11-02"
    ],
    "売上金額": [100000, 120000, 100000, 80000, 80000]
})


# データクレンジングから出力まで
def df_merge_print(df1, df2):
    # データクレンジング
    df2["店舗名_正規化"] = (
        df2["店舗名"]
        .str.replace(" ", "", regex=False)
        .str.replace("　", "", regex=False)
    )

    # データ結合
    df = pd.merge(df1, df2, left_on="店舗名", right_on="店舗名_正規化", how="left")

    # データ整形
    df = df[["店舗名_x", "売上比率", "売上金額"]]
    df = df.rename(columns={"店舗名_x": "店舗名"})
    print(df)

    # 売上合計金額・売上合計比率・売上最大店舗出力
    print(f"売上合計金額: {df['売上金額'].sum():,}円")
    print(f"売上合計比率: {df['売上比率'].sum():.1f}%")
    print(f"売上最大店舗: {df.loc[df['売上金額'].idxmax(), '店舗名']}")

# 重複削除
def duplication_delete(df3):
    # データ確認
    print(df3)

    # 重複データ削除
    df_clean = df3.drop_duplicates()
    print(df_clean)

    # 重複前後の売上金額の差分確認
    over_amount = df3["売上金額"].sum() - df_clean["売上金額"].sum()
    print(over_amount)

    print(f"重複削除前の売上合計: {df3['売上金額'].sum()}, 重複削除後の売上合計: {df_clean['売上金額'].sum()}, 重複によって過大計上されていた金額: {over_amount}")

def subset_delete(df4):
    print(df4)

    # 重複データ確認
    check = df4[df4.duplicated(subset=["店舗名", "日付"], keep=False)]
    
    print("\n--- 重複チェック ---")
    if check.empty:
        print("重複データはありません。")
    else:
        print("以下のデータが重複しています：")
        print(check)

    # 重複データ削除（最初に見つかった行を残す）
    clean_df = df4.drop_duplicates(subset=["店舗名", "日付"], keep="first")
    
    print("\n--- 重複削除後 ---")
    print(clean_df)

    return clean_df

# グルーピング
def group_by_sum(df5):
    before_total = df5['売上金額'].sum()
    print(f"集計前の売上金額:{before_total}")

    df_grouped = df5.groupby(["店舗名", "日付"])["売上金額"].sum().reset_index()
    after_total = df_grouped['売上金額'].sum()
    print(f"集計後の売上金額:{after_total}")

    if before_total == after_total:
        print("整合性チェック：OK")
    else:
        diff = abs(after_total - before_total)
        print(f"整合性チェック：NG\n差額:{diff:,}")

    return(df_grouped)


df_correct = pd.DataFrame({
    "店舗名": ["東京店", "大阪店", "名古屋店"],
    "売上金額": [100000, 80000, 90000]
})

df_result = pd.DataFrame({
    "店舗名": ["東京店", "大阪店", "福岡店"],
    "売上金額": [None, 80000, 50000]
})


# 店舗別整合性チェック
def check_store_consistency(df_correct, df_result):
    df = pd.merge(df_correct, df_result, on="店舗名", how="outer", indicator=True)

    # グループの分類
    both_df = df[df["_merge"] == "both"].copy()
    both_df["差額"] = both_df["売上金額_y"] - both_df["売上金額_x"]
    left_only_df = df[df["_merge"] == "left_only"]
    right_only_df = df[df["_merge"] == "right_only"]

    # both_dfで差額0ではないデータを抽出
    diff_df = both_df[both_df["差額"] != 0]

    # 判定処理
    if left_only_df.empty and right_only_df.empty and diff_df.empty:
        print("\n店舗別整合性チェック：OK")
    else:
        print("\n店舗別整合性チェック：NG")
        for _, row in left_only_df.iterrows():
            print(f"{row['店舗名']}:売上データなし")

        for _, row in right_only_df.iterrows():
            print(f"{row['店舗名']}:基準データなし")

        for _, row in diff_df.iterrows():
            if pd.isna(row['売上金額_x']) and pd.isna(row['売上金額_y']):
                print(f"{row['店舗名']}: 基準・売上ともに金額が欠損")
            elif pd.isna(row['売上金額_x']):
                print(f"{row['店舗名']}: 基準データの金額が欠損")
            elif pd.isna(row['売上金額_y']):
                print(f"{row['店舗名']}: 売上データの金額が欠損")
            else:
                print(f"{row['店舗名']}:差額{int(row['差額']):,}円")

    

# 実行
if __name__ == "__main__":
    check_store_consistency(df_correct, df_result)
