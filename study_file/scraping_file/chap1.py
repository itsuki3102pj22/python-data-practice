import requests
from bs4 import BeautifulSoup

# Webページ解析
load_url = "https://www.ymori.com/books/python2nen/test1.html"
html = requests.get(load_url)

soup = BeautifulSoup(html.content, "html.parser")

print(soup.find("title").text)
print(soup.find("h2").text)
print(soup.find("li").text)
