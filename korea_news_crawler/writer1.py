import csv
import platform


class Writer_press(object):
    def __init__(self, category_name):
        self.user_operating_system = str(platform.system())

        self.category_name = category_name
        # 이부분 추가
        self.text_company = 'aa'
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
        if self.user_operating_system == "Windows":
            self.file = open('Article_' + self.category_name + '_' + str(self.text_company) + '.csv', 'w',
                             encoding='euc-kr',
                             newline='')
        # Other OS uses utf-8
        else:
            self.file = open('Article_' + self.category_name + '_' + str(self.text_company) + '.csv', 'w',
                             encoding='utf-8',
                             newline='')

    def get_writer_csv(self):
        return self.wcsv

    def close(self):
        self.file.close()
