import requests
import time
import random
from bs4 import BeautifulSoup
from urllib.parse import urlparse

base_url = 'https://movie.naver.com/movie/point/af/list.nhn?&page={}'
#결과 저장할 리스트
comment_list = []
for page in range(1, 101):
    url = base_url.format(page)
    res=requests.get(url)
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, 'lxml')
        tds = soup.select('table.list_netizen > tbody > tr > td.title')
        for td in tds:
            movie_title = td.select_one('a.movie').text.strip()
            link = td.select_one('a.movie').get('href')
            link = parse.urljoin(base_url, link)
            score = td.select_one('div.list_netizen_score > em').text.strip()
            comment = td.select_one('br').next_sibling.strip()
            # 리스트에 저장
            comment_list.append((movie_title, link, score, comment))
        interval = round(random.uniform(0.2, 1.2), 2)
        time.sleep(interval)
print('종료') 