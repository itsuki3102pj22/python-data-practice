import requests
from bs4 import BeautifulSoup

load_url = "https://www.ymori.com/books/python2nen/test2.html"
html = requests.get(load_url)
soup = BeautifulSoup(html.content, "html.parser")

#print(soup)


# id=chap1の取得
#chap1 = soup.find(id="chap1")
#print(chap1.text)


# chap2の全てのliタグを取得
chap2 = soup.find(id="chap2")
for element in chap2.find_all("li"):
    print(element.text)

