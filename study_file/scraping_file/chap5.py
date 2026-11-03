import requests
from bs4 import BeautifulSoup
import urllib
from pathlib import Path

out_folder = Path("download")
out_folder.mkdir(exist_ok=True)

# 画像をダウンロード
load_url = "https://www.ymori.com/books/python2nen/test2.html"
html = requests.get(load_url)
soup = BeautifulSoup(html.content, "html.parser")

img_urls = []

for element in soup.find_all("img"):
    url = element.get("src")
    img_url = urllib.parse.urljoin(load_url, url)
    img_urls.append(img_url)

for img_url in img_urls:
    img = requests.get(img_url)
    fileName = img_url.split("/")[-1]
    out_file = out_folder.joinpath(fileName)
    with open(out_file, mode="wb") as f:
        f.write(img.content)