import requests
from bs4 import BeautifulSoup

# 青空文庫でスクレイピング
# 1.芥川龍之介_蜘蛛の糸
load_urls = ["https://www.aozora.gr.jp/cards/000879/files/92_14545.html", "https://www.aozora.gr.jp/cards/000153/files/816_15786.html", "https://www.aozora.gr.jp/cards/002240/files/61619_78128.html"]

for load_url in load_urls:
    html = requests.get(load_url)
    soup = BeautifulSoup(html.content, "html.parser")

    title =soup.find("h1", class_="title").text
    print("タイトル:", title)
    author = soup.find("h2", class_="author").text
    print("著者:", author)
    content = soup.find("div", class_="main_text").text
    print("本文:", content[:100])

