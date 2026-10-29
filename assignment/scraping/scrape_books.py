import requests
from bs4 import BeautifulSoup
import urllib
import csv

# データ取得
load_url = "https://books.toscrape.com"
html = requests.get(load_url, timeout=10)
# 取得できない場合は例外を発生させる
html.raise_for_status()

soup = BeautifulSoup(html.content, "html.parser")


# データ抽出
# 商品名｜価格｜在庫状況｜評価｜URLを抽出
books = []
for book in soup.select(".product_pod"):
    title = book.select_one("h3 a")["title"]
    price = book.select_one(".price_color").get_text(strip=True)
    stock = book.select_one(".availability").get_text(strip=True)
    stars = book.select_one(".star-rating")["class"][1]
    url = book.select_one("h3 a")["href"]

    # URLを絶対値に変換
    link_url = urllib.parse.urljoin(load_url, url)

    # 　データをリストに追加
    books.append(
        {
            "title": title,
            "price": price,
            "stock": stock,
            "stars": stars,
            "url": link_url,
        }
    )
# CSVファイルに保存
fileName = "books.csv"

with open(fileName, mode="w", encoding="utf-8", newline="") as f:
    fieldnames = ["title", "price", "stock", "stars", "url"]

    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(books)

print(f"{len(books)}件の商品を保存しました。")
