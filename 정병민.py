'''
articlecrawler.py에서 writer클래스 사용한 부분은 크게 2곳이다.
------95번째 ~ 96번째 줄------------------------------------------------
#Writer Class 생성
        writer = Writer(category_name=category_name, date=self.date)
----------------------------------------------------------------------

--------------160번째 ~ 172번째 줄--------------------------------------
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
----------------------------------------------------------------------
언론사를 사용자가 지정을 하면 date와 text_company를 csv파일에 저장할 필요가 없어진다.
****그리고 언론사는 Articlecrawler 클래스에 self.selected_text_company에 저장되고 크롤링 과정에선 text_company에 저장된다고 가정하자!!!!***
'''
#95번째 줄 변경
writer = Writer(category_name=category_name, text_company=text_company)

#162번째 줄 변경
wcsv.writerow([news_date, category_name, text_company, text_headline, text_sentence, content_url])

'''
writer.py 에서 변경할 부분 1
    def __init__(self, category_name, date):
        self.user_operating_system = str(platform.system())

        self.category_name = category_name

        self.date = date
        self.save_start_year = self.date['start_year']
        self.save_end_year = self.date['end_year']
        self.save_start_month = None
        self.save_end_month = None
        self.initialize_month()

        self.file = None
        self.initialize_file()

        self.wcsv = csv.writer(self.file)
       
'''


def __init__(self, category_name, date, text_company):
    self.user_operating_system = str(platform.system())

    self.category_name = category_name
    #이부분 추가
    self.text_company = text_company
    #
    self.date = date
    self.save_start_year = self.date['start_year']
    self.save_end_year = self.date['end_year']
    self.save_start_month = None
    self.save_end_month = None
    self.initialize_month()


    self.file = None
    self.initialize_file()

    self.wcsv = csv.writer(self.file)

'''
writer.py 에서 변경할 부분 2
    def initialize_file(self):
        if self.user_operating_system == "Windows":
            self.file = open('Article_' + self.category_name + '_' + str(self.save_start_year) + self.save_start_month
                             + '_' + str(self.save_end_year) + self.save_end_month + '.csv', 'w', encoding='euc-kr',
                             newline='')
        # Other OS uses utf-8
        else:
            self.file = open('Article_' + self.category_name + '_' + str(self.save_start_year) + self.save_start_month
                             + '_' + str(self.save_end_year) + self.save_end_month + '.csv', 'w', encoding='utf-8',
                             newline='')
'''

def initialize_file(self):
    if self.user_operating_system == "Windows":
        self.file = open('Article_' + self.category_name + '_' + str(self.text_company) + '.csv', 'w', encoding='euc-kr',
                         newline='')
    # Other OS uses utf-8
    else:
        self.file = open('Article_' + self.category_name + '_' + str(self.text_company) + '.csv', 'w', encoding='utf-8',
                         newline='')
