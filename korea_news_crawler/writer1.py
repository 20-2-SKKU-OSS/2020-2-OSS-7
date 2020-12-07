import csv
import platform


class Writer_press(object):
    def __init__(self, category_name,text_c):
        self.user_operating_system = str(platform.system())

        self.category_name = category_name
        # 이부분 추가
        self.text_company = text_c
        #
        '''
        self.date = "date"
        self.save_start_year = self.date['start_year']
        self.save_end_year = self.date['end_year']
        self.save_start_month = None
        self.save_end_month = None
        이부분도 필요없어요..
        ''' 
        #self.initialize_month() 이 함수는 필요없습니다...

        self.file = None
        self.initialize_file()
        self.file_name = ''

        self.wcsv = csv.writer(self.file)

    def initialize_month(self):
        if len(str(self.date['start_month'])) == 1:
            self.save_start_month = "0" + str(self.date['start_month'])
        else:
            self.save_start_month = str(self.date['start_month'])
        if len(str(self.date['end_month'])) == 1:
            self.save_end_month = "0" + str(self.date['end_month'])
        else:
            self.save_end_month = str(self.date['end_month'])

    def initialize_file(self):
            self.file = open('Article_' +str(self.text_company)+ self.category_name + '_' +  '.csv', 'w',
                             encoding='utf-8',
                             newline='')

    def keyword_search(self, keyword):
        self.file_name = 'Article_' + str(self.text_company) + self.category_name + '_' + '.csv'
        search_file = open(self.file_name, 'r', encoding='utf-8')
        write_search = open('Keyword_Search_' + self.file_name, 'w', encoding='utf-8')
        wcsv = csv.writer(write_search)
        rdr = csv.reader(search_file)
        for line in rdr:
            if line[0].find(keyword) != -1:
                wcsv.writerow([line[0], line[1], line[2], line[3]])
        search_file.close()
        write_search.close()

    def get_writer_csv(self):
        return self.wcsv

    def close(self):
        self.file.close()
