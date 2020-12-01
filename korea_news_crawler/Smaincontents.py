import requests
from bs4 import BeautifulSoup
from articleparser import ArticleParser

headers = {'User-Agent':'Mozilla/5.0'}
b = requests.get('https://sports.news.naver.com/news.nhn?oid=215&aid=0000918970',headers = headers)
document = BeautifulSoup(b.content, 'html.parser')
tag_content = document.find_all('div', {'id': 'newsEndContents'})
text_sentence = ''
text_sentence = text_sentence + ArticleParser.clear_content(str(tag_content[0].find_all(text=True)))
