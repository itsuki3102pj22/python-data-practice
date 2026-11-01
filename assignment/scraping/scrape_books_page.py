import requests
from bs4 import BeautifulSoup
import urllib.parse
import csv

# URL
load_url = "https://books.toscrape.com/"

# 現在のURL
current_url = load_url

# 取得するページ数
page_count = 0

# 商品データを蓄積するリスト
books = []

while page_count < 3:

    # HTML取得
    html = requests.get(current_url, timeout=10)
    html.raise_for_status()

    soup = BeautifulSoup(html.content, "html.parser")

    # データ抽出
    for book in soup.select(".product_pod"):
        title = book.select_one("h3 a")["title"]
        price = book.select_one(".price_color").get_text(strip=True)
        stock = book.select_one(".availability").get_text(strip=True)
        stars = book.select_one(".star-rating")["class"][1]
        url = book.select_one("h3 a")["href"]

        link_url = urllib.parse.urljoin(current_url, url)

        books.append({
            "title": title,
            "price": price,
            "stock": stock,
            "stars": stars,
            "url": link_url,
        })

    page_count += 1

    print(f"{page_count}ページ目取得完了")

    # 次ページのリンクを取得
    next_page = soup.select_one("li.next a")

    # 次のページがなければ終了
    if next_page is None:
        break

    # 次のURLを作成
    current_url = urllib.parse.urljoin(
        current_url,
        next_page["href"]
    )

# CSV出力
filename = "books_page.csv"

with open(filename, mode="w", encoding="utf-8-sig", newline="") as f:
    fieldnames = ["title", "price", "stock", "stars", "url"]

    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(books)

print(f"{len(books)}件の商品を保存しました。")