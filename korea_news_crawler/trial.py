#!/usr/bin/env python
# -*- coding: utf-8, euc-kr -*-

from time import sleep
from bs4 import BeautifulSoup
from tqdm import tqdm
from tqdm import trange
from multiprocessing import Process

from exceptions import *
from articleparser import ArticleParser
from writer import Writer

from writer1 import Writer_press

import os
import platform
import calendar
import requests
import re


class ArticleCrawler(object):
    def __init__(self):
        self.categories = {'정치': 100, '경제': 101, '사회': 102, '생활문화': 103, '세계': 104, 'IT과학': 105, '오피니언': 110,
                           'politics': 100, 'economy': 101, 'society': 102, 'living_culture': 103, 'world': 104, 'IT_science': 105, 'opinion': 110}
        self.selected_categories = []
        self.date = {'start_year': 0, 'start_month': 0, 'end_year': 0, 'end_month': 0}
        self.user_operating_system = str(platform.system())

    #크롤링할 카테고리 설정
    def set_category(self, *args):
        for key in args:
            if self.categories.get(key) is None:
                raise InvalidCategory(key)
        self.selected_categories = args

    #이상한 날짜가 들어온 경우
    def set_date_range(self, start_year, start_month, end_year, end_month):
        args = [start_year, start_month, end_year, end_month]
        if start_year > end_year:
            raise InvalidYear(start_year, end_year)
        if start_month < 1 or start_month > 12:
            raise InvalidMonth(start_month)
        if end_month < 1 or end_month > 12:
            raise InvalidMonth(end_month)
        if start_year == end_year and start_month > end_month:
            raise OverbalanceMonth(start_month, end_month)
        for key, date in zip(self.date, args):
            self.date[key] = date
        print(self.date)
        
    @staticmethod
    def make_news_page_url(category_url, start_year, end_year, start_month, end_month):
        made_urls = []
        
        for year in range(start_year, end_year + 1):
            
            if start_year == end_year:
                year_startmonth = start_month
                year_endmonth = end_month
            else:
                if year == start_year:
                    year_startmonth = start_month
                    year_endmonth = 12
                elif year == end_year:
                    year_startmonth = 1
                    year_endmonth = end_month
                else:
                    year_startmonth = 1
                    year_endmonth = 12
            
            for month in range(year_startmonth, year_endmonth + 1):
                
                for month_day in range(1, calendar.monthrange(year, month)[1] + 1):
                    if len(str(month)) == 1:
                        month = "0" + str(month)
                    if len(str(month_day)) == 1:
                        month_day = "0" + str(month_day)
                        
                    # 날짜별로 Page Url 생성
                    url = category_url + str(year) + str(month) + str(month_day)

                    # totalpage는 네이버 페이지 구조를 이용해서 page=10000으로 지정해 totalpage를 알아냄
                    # page=10000을 입력할 경우 페이지가 존재하지 않기 때문에 page=totalpage로 이동 됨 (Redirect)
                    
                    totalpage = ArticleParser.find_news_totalpage(url + "&page=10000")
                    
                    for page in range(1, totalpage + 1):
                        made_urls.append(url + "&page=" + str(page))
        return made_urls

    @staticmethod
    def get_url_data(url, max_tries=10):
        headers = {'User-Agent':'Mozilla/5.0'}
        remaining_tries = int(max_tries)
        while remaining_tries > 0:
            try:
                return requests.get(url, headers=headers)
            except requests.exceptions:
                sleep(60)
            remaining_tries = remaining_tries - 1
        raise ResponseTimeout()

    def crawling(self, category_name):
        # Multi Process PID
        print(category_name + " PID: " + str(os.getpid()))    

        writer = Writer(category_name=category_name, date=self.date)
        
        # 기사 URL 형식
        url = "http://news.naver.com/main/list.nhn?mode=LSD&mid=sec&sid1=" + str(self.categories.get(category_name)) + "&date="

        # start_year년 start_month월 ~ end_year의 end_month 날짜까지 기사를 수집합니다.
        day_urls = self.make_news_page_url(url, self.date['start_year'], self.date['end_year'], self.date['start_month'], self.date['end_month'])
        print(category_name + " Urls are generated")
        print("The crawler starts")

        for URL in day_urls:
            
            regex = re.compile("date=(\d+)")
            news_date = regex.findall(URL)[0]

            request = self.get_url_data(URL)

            document = BeautifulSoup(request.content, 'html.parser')

            # html - newsflash_body - type06_headline, type06
            # 각 페이지에 있는 기사들 가져오기
            post_temp = document.select('.newsflash_body .type06_headline li dl')
            post_temp.extend(document.select('.newsflash_body .type06 li dl'))
            
            # 각 페이지에 있는 기사들의 url 저장
            post = []
            for line in post_temp:
                post.append(line.a.get('href')) # 해당되는 page에서 모든 기사들의 URL을 post 리스트에 넣음
            del post_temp

            for content_url in post:  # 기사 URL
                # 크롤링 대기 시간
                sleep(0.01)
                
                # 기사 HTML 가져옴
                request_content = self.get_url_data(content_url)
                try:
                    document_content = BeautifulSoup(request_content.content, 'html.parser')
                except:
                    continue

                try:
                    # 기사 제목 가져옴
                    tag_headline = document_content.find_all('h3', {'id': 'articleTitle'}, {'class': 'tts_head'})
                    text_headline = ''  # 뉴스 기사 제목 초기화
                    text_headline = text_headline + ArticleParser.clear_headline(str(tag_headline[0].find_all(text=True)))
                    if not text_headline:  # 공백일 경우 기사 제외 처리
                        continue

                    # 기사 본문 가져옴
                    tag_content = document_content.find_all('div', {'id': 'articleBodyContents'})
                    text_sentence = ''  # 뉴스 기사 본문 초기화
                    text_sentence = text_sentence + ArticleParser.clear_content(str(tag_content[0].find_all(text=True)))
                    if not text_sentence:  # 공백일 경우 기사 제외 처리
                        continue

                    # 기사 언론사 가져옴
                    tag_company = document_content.find_all('meta', {'property': 'me2:category1'})
                    text_company = ''  # 언론사 초기화
                    text_company = text_company + str(tag_company[0].get('content'))
                    if not text_company:  # 공백일 경우 기사 제외 처리
                        continue
                        
                    # CSV 작성
                    wcsv = writer.get_writer_csv()
                    wcsv.writerow([news_date, category_name, text_company, text_headline, text_sentence, content_url])
                    
                    del text_company, text_sentence, text_headline
                    del tag_company 
                    del tag_content, tag_headline
                    del request_content, document_content

                except Exception as ex:  # UnicodeEncodeError ..
                    # wcsv.writerow([ex, content_url])
                    del request_content, document_content
                    pass
        writer.close()

    def article_inputTime(self, article_input):
        input_year = int(article_input[0:4])
        input_month = int(article_input[5:7])
        input_date = int(article_input[8:10])
        # csv 파일 생성을 위해 정보를 보내는 코드 필요

    def press_crawling(self, oid=215, aid=20):
        headers = {'User-Agent':'Mozilla/5.0'}
        writer = Writer_press(category_name = "aid123")
        url = 'https://sports.news.naver.com/news.nhn?'
        oid = 'oid='+str(oid)  
        #여기서 입력받은 oid(언론사 id)를 지정할 거에요
        for i in tqdm(range(1,aid), desc="Crawling rate", mininterval=0.01):
            #print(i)
            aid = str(i)
            aid_length = len(aid)
            aid = '&aid='+'0'*(10-aid_length) + aid
            url1 = url + oid + aid
            b = requests.get(url1,headers=headers)
            #print(url1)
            document = BeautifulSoup(b.content, 'html.parser')
            tag_content = document.find_all('div', {'id': 'newsEndContents'})
            
            text_sentence = ''
            text_sentence = text_sentence + ArticleParser.clear_content(str(tag_content[0].find_all(text=True)))
            #print(text_sentence)
            headline = ''
            tag_headline = document.find_all('h4', {'class':'title'})
            headline = headline + ArticleParser.clear_headline(str(tag_headline[0].find_all(text=True)))
            article_info = document.find_all('div',{'class':'info'})
            
            #기사 입력 시간 정보 받기
            tmp = str(article_info[0])
            article_input = tmp[30:41]

            input_year = int(article_input[0:4])
            input_month = int(article_input[5:7])
            input_date = int(article_input[8:10])

            #여기서 article info 정제 작업을 하며 좋을 것 같아요.
            writer.wcsv.writerow([headline,text_sentence,url1])
            print()
        writer.close()

        '''
        b = requests.get('https://sports.news.naver.com/news.nhn?oid=215&aid=0000918970',headers = headers)
        document = BeautifulSoup(b.content, 'html.parser')
        tag_content = document.find_all('div', {'id': 'newsEndContents'})
        text_sentence = '' #기사 본문입니다.
        text_sentence = text_sentence + ArticleParser.clear_content(str(tag_content[0].find_all(text=True)))
        headline = '' #기사 제목입니다.
        headline = headline + ArticleParser.clear_headline(str(document.find_all('h4', {'class':'title'})))
        article_info = document.find_all('div',{'class':'info'}) #기사 정보입니다.
        article_time = '2020.11.30. 오전 08:05'
        article_press = 'sbs스포츠'
        article_url = 'https://sports.news.naver.com/news.nhn?oid=215&aid=0000918970'
        '''
    def start(self):
        # MultiProcess 크롤링 시작
        for category_name in self.selected_categories:
            proc = Process(target=self.crawling, args=(category_name,))
            proc.start()
            self.crawling("생활문화")


if __name__ == "__main__":
    Crawler = ArticleCrawler()

    Crawler.set_category("생활문화")
    print("카테고리를 정해주세요")
    print("1. 정치")
    print("2. 경제")
    print("3. 사회")
    print("4. 생활문화")
    print("5. 세계")
    print("6. IT과학")
    print("7. 오피니언")
   # print("카테고리를 모두 골랐으면 quit을 입력하세요")
    #list1=[]
    s1=input('원하는 카테고리를 한글로 쓰고 엔터를 눌러주세요: ')
    #list1.append(s)
    a=int(input('원하는 크롤링할 범위의 시작년도: '))	
    b=int(input('원하는 크롤링할 범위의 시작 월: '))	
    c=int(input('원하는 크롤링할 범위의 끝 년도: '))	
    d=int(input('원하는 크롤링할 범위의 끝 년도: '))	
    
    Crawler.set_date_range(a, b, c, d)
    Crawler.set_category(s1)
    '''

    Crawler.set_category("생활문화", "IT과학")
    Crawler.set_date_range(2017, 1, 2017, 4)
    Crawler.start()
    '''
    #언론사별 크롤링 실행 함수입니다. 일단 oid aid는 default값을 설정했어요
    #Crawler.start()
    Crawler.press_crawling()
