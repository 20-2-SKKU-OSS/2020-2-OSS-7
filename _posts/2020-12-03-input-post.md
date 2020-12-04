---
title: 콘솔창에서 input으로 입력값들 받고 다른 함수에 전달해주는 함수 구현
categories: [SeoUitae]
comments: true
---
----------------------------------------------------------------------  
    Crawler = ArticleCrawler()
    print("카테고리를 정해주세요")
    print("1. 정치")
    print("2. 경제")
    print("3. 사회")
    print("4. 생활문화")
    print("5. 세계")
    print("6. IT과학")
    print("7. 오피니언")
  
    s1=input('원하는 카테고리를 한글로 쓰고 엔터를 눌러주세요: ')
    a=int(input('원하는 크롤링할 범위의 시작년도: '))	
    b=int(input('원하는 크롤링할 범위의 시작 월: '))	
    c=int(input('원하는 크롤링할 범위의 끝 년도: '))	
    d=int(input('원하는 크롤링할 범위의 끝 년도: '))	
    
    Crawler.set_date_range(a, b, c, d)
    Crawler.set_category(s1)
   
    Crawler.start()
    Crawler.press_crawling()
----------------------------------------------------------------------      







main 함수 내부에 일단 수정해두었는데, 이런 식으로 간단하게 구현할 수 있다.
set_date_range함수의 인자가 시작년도, 시작월, 끝 년도, 끝 월이므로 input 값을 int값으로 받은 뒤 넣어주고
카테고리를 문자열의 형태로 받아 넣어주면된다.
카테고리를 여러개 받아서 공백단위로 잘라서 리스트에 넣고 입력값으로 넣을 수 있게 해주려하였으나, 
우리의 목표는 기존 크롤러를 더 쉽고 편하게 사용하고 보완하는 것인데, 기존 크롤러의 가장 큰 문제점이 크롤링하는 시간이 매우 오래걸리고
진행상황을 알 수 없어 답답하다는 점이었는데, 이를 해결하려면 한 번에 여러개의 카테고리를 input으로 받는 것보다 한 가지만 받도록 crawling하고
끝난 뒤에 다시 다른 카테고리를 입력하여 crawling하는 것이 바람직하다고 생각하여 카테고리 input은 카테고리 한가지만을 받는 것으로 하였다.
추가적으로 기존 크롤러의 start함수 내부에 크롤러 실행을 위해  self.crawling("생활문화")를 추가해두었고,
    
    
    
    
----------------------------------------------------------------------      
    def start(self):
        # MultiProcess 크롤링 시작
        for category_name in self.selected_categories:
            proc = Process(target=self.crawling, args=(category_name,))
            proc.start()
 ----------------------------------------------------------------------            
  
  
이를 self.crawling(category_name)으로 수정하였다.
  
 ----------------------------------------------------------------------     
        def start(self):
        # MultiProcess 크롤링 시작
        for category_name in self.selected_categories:
            proc = Process(target=self.crawling, args=(category_name,))
            proc.start()
            self.crawling(category_name)
 ----------------------------------------------------------------------  
   
