import requests
from bs4 import BeautifulSoup
import urllib.parse
import csv

# URLを指定
load_url = "https://books.toscrape.com"

# データ取得
html = requests.get(load_url, timeout=10)
# 取得できない場合は例外を発生させる
html.raise_for_status()

soup = BeautifulSoup(html.content, "html.parser")

next_page = soup.select_one("li.next a")["href"]
# print(next_page)
# print(next_page["href"])

next_html = requests.get(urllib.parse.urljoin(load_url, next_page), timeout=10)
next_html.raise_for_status()
next_soup = BeautifulSoup(next_html.content, "html.parser")
# print(next_soup.prettify())

# データ抽出
# 商品名｜価格｜在庫状況｜評価｜URLを抽出
books = []
for book in next_soup.select(".product_pod"):
    title = book.select_one("h3 a")["title"]
    price = book.select_one(".price_color").get_text(strip=True)
    stock = book.select_one(".availability").get_text(strip=True)
    stars = book.select_one(".star-rating")["class"][1]
    url = book.select_one("h3 a")["href"]

    # URLを絶対値に変換
    link_url = urllib.parse.urljoin(load_url, url)

    books.append(
        {
            "title": title,
            "price": price,
            "stock": stock,
            "stars": stars,
            "url": link_url,
        }
    )
# print(books)
# CSVファイルに保存
fileName = "books_multi.csv"
with open(fileName, mode="w", encoding="utf-8", newline="") as f:
    fieldnames = ["title", "price", "stock", "stars", "url"]

    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(books)

print(f"{len(books)}件の商品を保存しました。")
