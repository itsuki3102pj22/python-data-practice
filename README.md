# Python実務・データ分析の学習

Pythonで、Webからのデータ収集、CSV・Excelの加工と可視化、売上レポートの作成、SQLiteを使った集計と照合を学ぶリポジトリです。処理ごとの実行方法と、必要な入力ファイルを以下にまとめています。

## ディレクトリ構成

```text
assignment/
├── scraping/                     # 書籍情報の取得とCSV出力
├── graph_generation/             # 商品データの抽出・グラフ描画・Excel加工
└── sales_report/
    ├── sales_products/           # 商品別の売上集計とExcelレポート
    │   ├── data/                  # 商品データ
    │   └── output/                # 保存済みの出力例
    └── sales_products2/          # 店舗別売上の分析とSQLite・pandasの練習
        ├── data/                  # 店舗別の売上CSVと売上目標
        └── output/                # 保存済みのCSV・グラフ・Excel
```

## 環境準備

リポジトリのルートで実行します。

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install requests beautifulsoup4 pandas matplotlib openpyxl pillow
```

SQLiteにはPython標準ライブラリの `sqlite3` を使用します。日本語のグラフラベルには、各スクリプトのMatplotlib設定で利用できる日本語フォントが必要です。

## 書籍情報の取得

練習用サイト Books to Scrape から、書名・価格・在庫・評価・商品リンクを取得します。インターネット接続が必要で、CSVは実行したディレクトリに上書き保存されます。

| スクリプト | 取得範囲 | 出力 |
| --- | --- | --- |
| `scrape_books.py` | 最初の一覧ページ | `books.csv` |
| `scrape_books_multi.py` | 最初のページから次へ進み、2ページ目の商品を取得 | `books_multi.csv` |
| `scrape_books_page.py` | 次ページのリンクをたどり、最大3ページ | `books_page.csv`（BOM付きUTF-8） |

```sh
(cd assignment/scraping && python scrape_books_page.py)
```

## 商品データの加工・可視化

`graph_generation/` で実行します。CSVを読む2本は入力をスクリプトと同じ場所に探すため、同梱サンプルを下のコマンドでコピーします。

| スクリプト | 入力と処理 |
| --- | --- |
| `read.py` | `products.csv` から商品名、単価5,000円以上の行、販売数10個以上の行、行数と列数を表示 |
| `plot_data.py` | `sales_result.csv` の先頭列を商品名のインデックスとして読み、売上金額と販売数の棒グラフを表示し、実行ディレクトリにPNGを保存 |
| `execl_read.py` | 同じ場所の `sales.xlsx` を読み、2〜6行目の売上金額とD7の合計式を追加して `sales_updated.xlsx` に保存 |

```sh
(
  cd assignment/graph_generation
  cp ../sales_report/sales_products/data/products.csv .
  cp ../sales_report/sales_products/output/sales_result.csv .
  python read.py
  python plot_data.py
  python execl_read.py
)
```

## 商品別売上レポート

`sales_products/` の `process_data.py` と `sales_analysis.py` は、スクリプトと同じ場所の `products.csv` を読みます。同梱の入力は `data/` にあります。

```sh
(
  cd assignment/sales_report/sales_products
  cp data/products.csv .
  python process_data.py
  python sales_analysis.py
)
```

| スクリプト | 処理と出力 |
| --- | --- |
| `process_data.py` | 単価×販売数を計算し、商品別の販売数と売上金額を売上順に集計。スクリプトの隣に `sales_summary.csv` を保存 |
| `sales_analysis.py` | 商品別の売上金額と販売数の棒グラフを表示し、実行ディレクトリにPNGを保存。集計・合計式・画像を含む `monthly_sales_report.xlsx` をスクリプトの隣に保存 |
| `report.py` | 同じ場所の `sales_by_product.csv` を読み、売上金額列と合計行をメモリ上で追加する練習。先頭列をインデックスとして読み込むため、入力例は `商品名,分類,単価,販売数`。実行時のファイル出力はなし |

## 店舗別売上の分析・照合

```sh
python assignment/sales_report/sales_products2/main.py
python assignment/sales_report/sales_products2/database.py
```

- `main.py` の通常実行では、`data/store_target.csv` と `data/sales_*.csv` を読み込みます。売上CSVの空ファイルと必須列（日付・店舗名・商品名・単価・販売数）を確認し、結合後の列の型を表示します。
- 売上金額の計算と値の検証、店舗別・商品別・店舗×商品別の集計、目標達成率、日別売上と最高売上日、折れ線グラフ、Excelの出力・書式設定は関数として実装済みです。現在の `main()` ではこれらの呼び出しがコメントアウトされています。`output/sales_report.xlsx` とグラフは保存済みの出力例です。
- `database.py` の通常実行では、コード内のサンプルで店舗別整合性チェックを行い、店舗行の不在、金額の欠損、差額を表示します。CSV取込、SQLiteへのINSERT・UPSERT、SQL集計、pandasでの重複処理とCSV出力は関数を個別に呼び出して試せます。詳しくは[店舗別売上の学習メモ](assignment/sales_report/sales_products2/README.md)を参照してください。
