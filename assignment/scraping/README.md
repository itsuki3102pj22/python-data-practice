# Python Webスクレイピング学習

## 1. プロジェクト概要

Pythonを使用したWebスクレイピングの学習プロジェクトです。

書籍情報を掲載している練習用Webサイト「Books to Scrape」から商品情報を取得し、CSVファイルに保存するプログラムを作成しました。

基本的なWebスクレイピングから、複数ページのデータを自動取得する処理まで実装しています。

**学習目的**
- PythonによるWebスクレイピングの習得
- Webサイトからのデータ取得・抽出
- 取得したデータのCSV出力
- 複数ページの自動取得
- データ分析に向けた基礎知識の習得

## 2. 使用技術・ライブラリ

| 技術・ライブラリ | 用途 |
|---|---|
| Python | プログラミング言語 |
| Requests | WebサイトへのHTTPリクエスト |
| BeautifulSoup4 | HTMLの解析・データ抽出 |
| urllib.parse | URLの結合・変換 |
| csv | CSVファイルの作成・出力 |

## 3. 実装機能

### ① Webスクレイピング

Requestsを使用してWebサイトのHTMLを取得し、BeautifulSoupで解析しています。

CSSセレクタを使用して、必要な商品情報を抽出します。

### ② 商品情報の取得

以下の5項目を取得しています。

| 項目 | 取得内容 |
|---|---|
| 商品名 | 書籍のタイトル |
| 価格 | 書籍の販売価格 |
| 在庫状況 | 在庫の有無 |
| 評価 | 星による評価 |
| URL | 書籍の詳細ページURL |

### ③ 複数ページの自動取得

Webサイトの次ページへのリンクを取得し、複数ページの商品情報を自動で収集する処理を実装しました。

- HTMLから次ページのURLを取得
- `urllib.parse.urljoin()` による相対URLの変換
- `while` 文による繰り返し処理
- 取得したデータをリストに蓄積

現在は3ページ分、合計60冊の書籍情報を取得できます。

### ④ CSVファイルへの出力

取得した商品情報を辞書形式でリストに保存し、`csv.DictWriter` を使用してCSVファイルに出力します。

### ⑤ エラー処理

HTTPリクエストに関する基本的なエラー対策を実装しています。

- `timeout=10`：通信のタイムアウト設定
- `raise_for_status()`：HTTPエラーの検出

## 4. プロジェクトのディレクトリ構成

```text
Python/assignment/scraping
├── scrape_books.py
├── scrape_books_multi.py
├── books.csv
├── books_multi.csv
├── books_page.csv
├── README.md
└── .gitignore
```

※各ファイルの役割は以下のとおりです。

| ファイル | 内容 |
|---|---|
| `scrape_books.py` | 1ページ目の商品情報取得 |
| `scrape_books_multi.py` | 複数ページの商品情報取得 |
| `books.csv` | 1ページ目の取得データ |
| `books_multi.csv` | 2ページ目の取得データ |
| `books_page.csv` | 3ページ分の取得データ |

## 5. 実行方法

### 必要なライブラリのインストール

```bash
pip install requests beautifulsoup4
```

### プログラムの実行

複数ページのスクレイピングを実行する場合：

```bash
python scrape_books_multi.py
```

実行すると、取得した書籍情報がCSVファイルとして保存されます。

## 6. 学習内容・習得したこと

- Requestsを使用したHTTPリクエスト
- BeautifulSoupによるHTML解析
- CSSセレクタを使用したデータ抽出
- HTMLタグの属性とテキストの取得
- 相対URLと絶対URLの違い
- `urllib.parse.urljoin()` によるURL変換
- `for` 文・`while` 文を使用した繰り返し処理
- リストと辞書を使用したデータ管理
- CSVファイルへのデータ出力
- HTTP通信における基本的なエラー処理

## 7. 今後の学習予定

今回習得したスクレイピングの知識を活用し、データ分析まで一貫して実施できることを目標としています。

今後は以下の内容に取り組む予定です。

- Matplotlibを使用したデータの可視化
- Pandasを使用したデータの加工・集計
- スクレイピングしたデータの分析
- 商品価格や在庫状況の比較・分析
- 実務を想定したデータ収集・分析ツールの作成

---

**学習用サイト：** [Books to Scrape](https://books.toscrape.com/)

