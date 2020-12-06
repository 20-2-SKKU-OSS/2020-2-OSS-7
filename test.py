from korea_news_crawler import articlecrawler


Crawler = articlecrawler.ArticleCrawler()
oid_num, name = articlecrawler.get_oid()
print("몇 개의 기사를 크롤링 할까요?")
aid = int(input())
Crawler.press_crawling(oid = oid_num , aid = aid , name = name)
Crawler.keyword_search('조사')