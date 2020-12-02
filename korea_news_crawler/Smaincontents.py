import requests
from bs4 import BeautifulSoup
from articleparser import ArticleParser

headers = {'User-Agent':'Mozilla/5.0'}
b = requests.get('https://sports.news.naver.com/news.nhn?oid=215&aid=0000918970',headers = headers)
document = BeautifulSoup(b.content, 'html.parser')
tag_content = document.find_all('div', {'id': 'newsEndContents'})
text_sentence = ''
text_sentence = text_sentence + ArticleParser.clear_content(str(tag_content[0].find_all(text=True)))
headline = ''
headline = headline + ArticleParser.clear_headline(str(document.find_all('h4', {'class':'title'})))
article_info = document.find_all('div',{'class':'info'})
# text_sentence는 기사 본문을 저장한 값
# headline은 기사 제목을 저장한 값
'''
article_info는 기사 정보를 저장한 값
[<div class="info">
<span>기사입력 2020.11.30. 오전 08:05</span>
<span><span class="bar"></span>최종수정 2020.11.30. 오전 08:07</span>
<a class="press_link" href="http://www.wowtv.co.kr/NewsCenter/News/Read?articleId=A202011300032&amp;t=NN" target="_blank">기사원문</a>
</div>]
와 같은 형식으로 저장되어있음
'''