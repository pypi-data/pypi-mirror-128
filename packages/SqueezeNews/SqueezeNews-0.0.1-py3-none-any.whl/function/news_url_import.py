import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import os
import pandas as pd

def news_url_import(keyword, num):
    #input 생성, 검색할 키워드, 추출할 뉴스 기사 수 저장
    query = keyword
    query = query.replace(' ', '+')

    news_num = int(num)

    # 요청할 URL 생성 및 요청
    news_url = 'https://search.naver.com/search.naver?where=news&sm=tab_jum&query={}'

    req = requests.get(news_url.format(query))
    soup = BeautifulSoup(req.text, 'html.parser')

    # 뉴스 기사 정보를 저장할 딕셔너리 생성
    news_dict = {}
    idx = 0
    cur_page = 1

    while idx < news_num:

        table = soup.find('ul',{'class' : 'list_news'})
        li_list = table.find_all('li', {'id': re.compile('sp_nws.*')})
        area_list = [li.find('div', {'class' : 'news_area'}) for li in li_list]
        a_list = [area.find('a', {'class' : 'news_tit'}) for area in area_list]
        
        for n in a_list[:min(len(a_list), news_num-idx)]:
            news_dict[idx] = {'title' : n.get('title'),
                            'url' : n.get('href') }
            idx += 1

        cur_page += 1
        
        pages = soup.find('div', {'class' : 'sc_page_inner'})
        next_page_url = [p for p in pages.find_all('a') if p.text == str(cur_page)][0].get('href')
        
        req = requests.get('https://search.naver.com/search.naver' + next_page_url)
        soup = BeautifulSoup(req.text, 'html.parser')

    return news_dict
    # print(news_dict[0]['url'])
