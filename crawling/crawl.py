from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen("https://movie.naver.com/movie/bi/mi/basic.nhn?code=194205")

bsObject = BeautifulSoup(html, "html.parser")

#for link in bsObject.find_all('a'):
#    print(link.text.strip(), link.get('href'))

for link in bsObject.find_all('img'):
    print(link.text.strip(), link.get('src'))