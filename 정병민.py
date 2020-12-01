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
'''
#95번째 줄 변경
writer = Writer(category_name=category_name)

#162번째 줄 변경
wcsv.writerow([news_date, category_name, text_company, text_headline, text_sentence, content_url])
