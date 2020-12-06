#!/usr/bin/env python
# -*- coding: utf-8, euc-kr -*-

from time import sleep
from bs4 import BeautifulSoup
import threading
from tqdm import tqdm
from tqdm import trange
from multiprocessing import Process
from PyQt5.QtWidgets import * #QApplication, QWidget, QLabel, QTextEdit
from PyQt5.QtCore import pyqtSignal, QThread

from exceptions import *
from articleparser import ArticleParser
from writer import Writer

from writer1 import Writer_press
import sys
import os
import platform
import calendar
import requests
import re

def get_oid(oid_num):
        oid = ['001','005','009','014','629','018','021','022','047','052','055','065',' 469','088','108','109','117','119','139','144','236','277','311','343','347','356', '382','396','398','410','413','417','421','436','439','442','445','477','450','468']
        name = ["연합뉴스","국민일보","매일경제", "파이낸셜뉴스","더팩트","이데일리","문화일보","세계일보","오마이뉴스","YTN","SBS","점프볼","한국일보","매일신문","스타뉴스",
            "OSEN","마이데일리","데일리안","스포탈코리아","스포츠경향","포모스","아시아경제","엑스포츠뉴스","베스트일레븐","데일리e스포츠","게임메카","스포츠동아","스포츠월드","루키","MK스포츠",
            "인터풋볼","머니S","뉴스1","풋볼리스트","디스이즈게임","인벤","윈터뉴스","스포티비뉴스","STN 스포츠","스포츠서울"
        ]
        print("\n1.연합뉴스\n2.국민일보\n3.매일경제 \n4.파이낸셜뉴스\n5.더팩트\n6.이데일리\n7.문화일보\n8.세계일보\n9. 오마이뉴스\n10.YTN\n11.SBS\n12.점프볼\n13.한국일보\n14.매일신문\n15.스타뉴스") 
        print("16.OSEN\n17.마이데일리\n18.데일리안\n19.스포탈코리아\n20.스포츠경향\n21.포모스\n22.아시아경제\n23.엑스포츠뉴스\n24.베스트일레븐\n25.데일리e스포츠\n26.게임메카\n27.스포츠동아\n28.스포츠월드\n29.루키\n30.MK스포츠")
        print("31.인터풋볼\n32.머니S\n33.뉴스1\n34.풋볼리스트\n35.디스이즈게임\n36.인벤\n37.윈터뉴스\n38.스포티비뉴스\n39.STN 스포츠\n40.스포츠서울\n")
        #uinput = input("원하는 언론사 번호를 입력하세요: ")
        #oid_num = int(uinput)
        result = oid[oid_num-1]
        return result, name[oid_num-1]


class ArticleCrawler(object):
    def __init__(self):
        #self.initUI()
        self.categories = {'정치': 100, '경제': 101, '사회': 102, '생활문화': 103, '세계': 104, 'IT과학': 105, '오피니언': 110,
                           'politics': 100, 'economy': 101, 'society': 102, 'living_culture': 103, 'world': 104, 'IT_science': 105, 'opinion': 110}
        self.selected_categories = []
        self.date = {'start_year': 0, 'start_month': 0, 'end_year': 0, 'end_month': 0}
        self.user_operating_system = str(platform.system())
        self.writer = None
        self.made_urls = []
        self.num=0

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
    def make_news_page_url(self, category_url, start_year, end_year, start_month, end_month):
        
        
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
            
            for month in tqdm(range(year_startmonth, year_endmonth + 1),desc="MakeUrl rate", mininterval=0.01):
                print('\n')
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
                        self.made_urls.append(url + "&page=" + str(page))
        print("url개수: "+str(len(self.made_urls)))
        return self.made_urls

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

    # 기사 입력 시간 정보 받기
    @staticmethod
    def inputTime(input_time):
        article_input = input_time[30:40] #ex) "2020.06.11" 을 받음 / 예전꺼만 될 수도 있음. 크롤링하고 문제있으면 수정할 것
        return article_input

    def crawling(self, category_name):
        # Multi Process PID
        print(category_name + " PID: " + str(os.getpid()))    

        writer = Writer(category_name=category_name, date=self.date)
        self.writer = writer
        # 기사 URL 형식
        url = "http://news.naver.com/main/list.nhn?mode=LSD&mid=sec&sid1=" + str(self.categories.get(category_name)) + "&date="

        # start_year년 start_month월 ~ end_year의 end_month 날짜까지 기사를 수집합니다.
        day_urls = self.make_news_page_url(self, url, self.date['start_year'], self.date['end_year'], self.date['start_month'], self.date['end_month'])
        print(category_name + " Urls are generated")
        print("The crawler starts")


        for URL in tqdm(day_urls,desc="Crawling rate", mininterval=0.01):
            self.num+=1 
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

    def press_crawling(self, oid, aid, name):
        headers = {'User-Agent':'Mozilla/5.0'}
        
        url = 'https://sports.news.naver.com/news.nhn?'
        
        writer = Writer_press(category_name = str(aid),text_c=name )
        self.writer = writer

        oid = 'oid='+ oid
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
            
            if len(tag_content) != 0:
                    #print(url1)
                    text_sentence = ''
                    text_sentence = text_sentence + ArticleParser.clear_content(str(tag_content[0].find_all(text=True)))
                    #print(text_sentence)
                    headline = ''
                    tag_headline = document.find_all('h4', {'class':'title'})
                    headline = headline + ArticleParser.clear_headline(str(tag_headline[0].find_all(text=True)))
                    article_info = document.find_all('div',{'class':'info'})
                    #여기서 article info 정제 작업을 하며 좋을 것 같아요.

                    #====================================================
                    #기사 입력 시간 정보 받기
                    input_time = str(article_info[0])
                    iTime = ""
                    iTime = self.inputTime(input_time)
                    #print("\n")
                    #print(iTime)
                    #===================================================
                    if headline == '':
                        headline = '-'
                    writer.wcsv.writerow([headline,text_sentence,url1,iTime])
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
            self.crawling(category_name)

    def keyword_search(self, keyword):
        self.writer.keyword_search(keyword)


    def Keyword_crawling(self):
        headers = {'User-Agent':'Mozilla/5.0'}
        url = 'https://search.naver.com/search.naver?sm=tab_hty.top&where=news&query='
        url = url + keyword
        list_a = []
        for i in tqdm(range(0,20),desc="append url list", mininterval = 0.01):
            s_num = "&start="+str(i)+"1"
            b = requests.get(url+s_num, headers = headers)
            document = BeautifulSoup(b.content, 'html.parser')
            writer = Writer_press(category_name = '_'+keyword,text_c="Keyword_crawling" )
            list_url = document.select('.list_news .info')
            
            for line in list_url:
                list_a.append(line.get('href'))
                #print(line.get('href'))
            print('')
        list_b = []
        list_c = []
        for line in list_a:
            if(line == None):
                continue
            elif(line.find('naver') != -1):
                list_b.append(line)
        for line in list_b:
            fnum = line.find('oid')
            if len(line[fnum:]) == 22:
                list_c.append(line[fnum:])
        url = 'https://sports.news.naver.com/news.nhn?'
        list_num = len(list_c)
        print(list_c)
        for i in tqdm(range(0,list_num),desc="Crawling rate", mininterval=0.01):
            print('')
            url_a = url + list_c[i]
            b = requests.get(url_a,headers=headers)
            document = BeautifulSoup(b.content, 'html.parser')
            tag_content = document.find_all('div', {'id': 'newsEndContents'})
            if len(tag_content) != 0:
                text_sentence = ''
                text_sentence = text_sentence + ArticleParser.clear_content(str(tag_content[0].find_all(text=True)))
                headline = ''
                tag_headline = document.find_all('h4', {'class':'title'})
                if(len(tag_headline) != 0):
                    headline = headline + ArticleParser.clear_headline(str(tag_headline[0].find_all(text=True)))
                article_info = document.find_all('div',{'class':'info'})
                writer.wcsv.writerow([headline,text_sentence,url_a])

            self.crawling(category_name)


class gui(QWidget):  
    def __init__(self):
        super().__init__()
        self.initUI()
        #th=update()
        startYear=0
        startMonth=0
        endYear=0
        endMonth=0
        cat=0
        press=0
        num=0

    def initUI(self):
        self.Crawler = ArticleCrawler()
        label0=QLabel('크롤러를 설정해주세요.', self)
        label0.move(50, 30)
        font0=label0.font()
        font0.setBold(True)
        font0.setPointSize(14)
        label0.setFont(font0)

        self.rbtn1=QRadioButton('카테고리별 크롤링', self)
        self.rbtn2=QRadioButton('언론사별 크롤링', self)
        self.rbtn1.setChecked(True)
        self.rbtn1.move(50, 70)
        self.rbtn2.move(250, 70)
        self.rbtn1.clicked.connect(self.onClicked)
        self.rbtn2.clicked.connect(self.onClicked)
        
        
        self.catLabel=QLabel('1. 정치  2. 경제  3. 사회  4. 생활문화  5. 세계  6. IT과학  7. 오피니언', self)
        self.catLabel.move(50, 100)
        self.pressLabel=QLabel('1.연합뉴스 2.국민일보 3.매일경제 4.파이낸셜뉴스 5.더팩트 6.이데일리 7.문화일보 8.세계일보 9. 오마이뉴스 10.YTN \n\
11.SBS 12.점프볼 13.한국일보 14.매일신문 15.스타뉴스 16.OSEN 17.마이데일리 18.데일리안 19.스포탈코리아 20.스포츠경향\n\
21.포모스 22.아시아경제 23.엑스포츠뉴스 24.베스트일레븐 25.데일리e스포츠 26.게임메카 27.스포츠동아 28.스포츠월드 29.루키 30.MK스포츠\n\
31.인터풋볼 32.머니S 33.뉴스1 34.풋볼리스트 35.디스이즈게임 36.인벤 37.윈터뉴스 38.스포티비뉴스 39.STN 스포츠 40.스포츠서울', self)
        self.pressLabel.move(50, 100)
        self.pressLabel.hide()

        self.selectLabel1=QLabel('카테고리 선택 : ', self)
        self.selectLabel1.move(50, 130)
        self.catEdit=QLineEdit(self)
        self.catEdit.move(168, 128)
        self.catEdit.textChanged[str].connect(self.catChanged)

        self.timeLabel1=QLabel('시작 년도: ', self)
        self.timeEdit1=QLineEdit(self)
        self.timeLabel2=QLabel('시작 월: ', self)
        self.timeEdit2=QLineEdit(self)
        self.timeLabel3=QLabel('끝 년도: ', self)
        self.timeEdit3=QLineEdit(self)
        self.timeLabel4=QLabel('끝 월: ', self)
        self.timeEdit4=QLineEdit(self)
        self.timeLabel1.move(50, 160)
        self.timeEdit1.move(130, 158)
        self.timeLabel2.move(340, 160)
        self.timeEdit2.move(400, 158)
        self.timeLabel3.move(50, 190)
        self.timeEdit3.move(120, 188)
        self.timeLabel4.move(320, 190)
        self.timeEdit4.move(370, 188)

        self.timeEdit1.textChanged[str].connect(self.timeChanged1)
        self.timeEdit2.textChanged[str].connect(self.timeChanged2)
        self.timeEdit3.textChanged[str].connect(self.timeChanged3)
        self.timeEdit4.textChanged[str].connect(self.timeChanged4)

        self.btn1=QPushButton(self)
        self.btn1.setText('크롤링 시작')
        self.btn1.move(50, 225)
        self.btn1.clicked.connect(self.btn1Clicked)

        self.btn3=QPushButton(self)
        self.btn3.setText('진행상황')
        self.btn3.move(50, 300)
        self.btn3.clicked.connect(self.btn3Clicked)

        
        self.pbar=QProgressBar(self)
        self.pbar.setGeometry(50, 270, 400, 30)
        
        self.option1=[self.selectLabel1, self. catLabel, self.catEdit, self.timeLabel1, self.timeLabel2, self.timeLabel3, self.timeLabel4,\
            self.timeEdit1, self.timeEdit2, self.timeEdit3, self.timeEdit4, self.btn1, self.btn3]

        self.selectLabel2=QLabel('언론사 선택 : ', self)
        self.selectLabel2.move(50, 180)
        self.pressEdit=QLineEdit(self)
        self.pressEdit.move(155, 180)
        self.numLabel=QLabel('크롤링할 기사의 개수: ', self)
        self.numLabel.move(50, 210)
        self.numEdit=QLineEdit(self)
        self.numEdit.move(210, 208)

        self.pressEdit.textChanged[str].connect(self.pressChanged)
        self.numEdit.textChanged[str].connect(self.numChanged)

        self.btn2=QPushButton(self)
        self.btn2.setText("크롤링 시작")
        self.btn2.move(50, 250)
        self.btn2.clicked.connect(self.btn2Clicked)
        self.option2=[self.pressLabel, self.selectLabel2, self.pressEdit, self.numLabel, self.numEdit, self.btn2]
        

        for option in self.option2:
            option.hide()
        self.resize(1100, 800)
        self.setWindowTitle("뉴스 기사 크롤링")
        self.show() 

    def onClicked(self):
        if self.rbtn1.isChecked():
            for option in self.option2:
                option.hide()
            for option in self.option1:
                option.show()
        if self.rbtn2.isChecked():
            for option in self.option1:
                option.hide()
            for option in self.option2:
                option.show()
    
    def catChanged(self, num):
        if num:
            self.cat=int(num)
    def timeChanged1(self, num):
        if num:
            self.startYear=int(num)
    def timeChanged2(self, num):
        if num:
            self.startMonth=int(num)
    def timeChanged3(self, num):
        if num:
            self.endYear=int(num)
    def timeChanged4(self, num):
        if num:
            self.endMonth=int(num)
    def pressChanged(self, num):
        if num:
            self.press=int(num)
    def numChanged(self, num):
        if num:
            self.num=int(num)
    def btn1Clicked(self):
        if self.cat == 1 :
            ss1 = "정치"
        if self.cat == 2 :
            ss1 = "경제"
        if self.cat == 3 :
            ss1 = "사회"
        if self.cat == 4 :
            ss1 = "생활문화"
        if self.cat == 5 :
            ss1 = "세계"
        if self.cat == 6 :
            ss1 = "IT과학"
        if self.cat == 7 :
            ss1 = "오피니언"
        Crawler.set_category(ss1)
        Crawler.set_date_range(self.startYear, self.startMonth, self.endYear, self.endMonth)
        #self.Crawler.start()
        x=update(self)
        x.start()
        
    def btn2Clicked(self):
        oid, name = get_oid(self.press)
        Crawler.press_crawling(oid = oid, aid = self.num, name = name)
        
    def btn3Clicked(self):
        if len(Crawler.made_urls) !=0 :
            value=(Crawler.num/len(Crawler.made_urls))*100
            self.pbar.setValue(value)
        print(str(value))
    

class update(QThread):
    def run(self):
        Crawler.start()
        
Crawler = ArticleCrawler()
if __name__ == "__main__": 
    app=QApplication(sys.argv)
    w=gui()
    #sys.exit(app.exec_())
    
    print("1.카테고리 별 크롤링(정치,경제,사회,생활문화...) 2.언론사별 크롤링 3.키워드 크롤링(약간의 오류가 존재)")
    select = int(input())
    #Crawler.set_category("생활문화")
    if(select == 1):
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
            s1=int(input('원하는 카테고리 번호를 입력하고 엔터를 눌러주세요: '))
            #list1.append(s)
            a=int(input('원하는 크롤링할 범위의 시작년도: '))	
            b=int(input('원하는 크롤링할 범위의 시작 월: '))	
            c=int(input('원하는 크롤링할 범위의 끝 년도: '))	
            d=int(input('원하는 크롤링할 범위의 끝 년도: '))	
            ss1 = "정치"

            if s1 == 1 :
              ss1 = "정치"
            if s1 == 2 :
              ss1 = "경제"
            if s1 == 3 :
              ss1 = "사회"
            if s1 == 4 :
              ss1 = "생활문화"
            if s1 == 5 :
              ss1 = "세계"
            if s1 == 6 :
              ss1 = "IT과학"
            if s1 == 7 :
              ss1 = "오피니언"
            Crawler.set_date_range(a,b,c,d)
            Crawler.set_category(ss1)
            Crawler.start()
              
    if(select == 2):
            oid_num, name = get_oid()
            print("몇 개의 기사를 크롤링 할까요?")
            aid = int(input())
            Crawler.press_crawling(oid = oid_num , aid = aid , name = name)
    if(select == 3):
            print("검색할 단어를 입력해 주세요:")
            keyword = input()
            Crawler.Keyword_crawling(keyword = keyword)
    

    Crawler.set_date_range(a, b, c, d)
    Crawler.set_category(ss1)
    #Crawler.press_crawling()


