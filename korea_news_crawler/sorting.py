import pandas as pd

a=int(input("어느 크롤러로 크롤링한 csv파일인가요?\n1번 2번\n"))

#2번 크롤러를 선택했을 때 
if(a==2):

	b=input("파일명을 입력해주세요:")
	#df1=pd.read_csv('Article_10_문화일보.csv', names=['A','B','C','D'])
	df1=pd.read_csv(b, names=['A','B','C','D'])
	print(df1)
	c=int(input('어떻게 정렬할까요? \n1.오래된 순으로 정렬\n2.최신순으로 정렬\n'))
	if(c==1):
		df2=df1.sort_values(by=['D'])
		df2=df2.reset_index(drop=True)
		print(df2)
		d=input('위와 같이 정렬된 파일을 저장하시겠습니까?(y/n)')
		if(d=='y'):
			e=input('파일명은 result.csv파일로 저장됩니다. 다른 이름을 원하시면 n을 눌러주세요.(y/n)')
			if(e=='y'):		
				df2.to_csv("result.csv")
				print('저장이 완료되었습니다.')
			if(e=='n'):
				f=input('파일명을 입력해주세요: ')
				df2.to_csv(f)
				print('저장이 완료되었습니다.')
	if(c==2):
		df2=df1.sort_values(by=['D'],ascending=[False])
		df2=df2.reset_index(drop=True)
		print(df2)
		d=input('위와 같이 정렬된 파일을 저장하시겠습니까?(y/n)')
		if(d=='y'):
			e=input('파일명은 result.csv파일로 저장됩니다. 다른 이름을 원하시면 n을 눌러주세요.(y/n)')
			if(e=='y'):		
				df2.to_csv("result.csv")
				print('저장이 완료되었습니다.')
			if(e=='n'):
				f=input('파일명을 입력해주세요: ')
				df2.to_csv(f)
				print('저장이 완료되었습니다.')
#1번 크롤러를 선택했을 때 
if(a==1):

	b=input("파일명을 입력해주세요:")
	#df1=pd.read_csv('Article_오피니언_202009_202009.csv',names=['A','B','C','D','E','F'])
	df1=pd.read_csv(b, names=['A','B','C','D','E','F'])
	print(df1)
	c=int(input('어떻게 정렬할까요? \n1.오래된 순으로 정렬\n2.최신순으로 정렬\n'))
	if(c==1):
		df2=df1.sort_values(by=['A'])
		df2=df2.reset_index(drop=True)
		print(df2)
		d=input('위와 같이 정렬된 파일을 저장하시겠습니까?(y/n)')
		if(d=='y'):
			e=input('파일명은 result.csv파일로 저장됩니다. 다른 이름을 원하시면 n을 눌러주세요.(y/n)')
			if(e=='y'):		
				df2.to_csv("result.csv")
				print('저장이 완료되었습니다.')
			if(e=='n'):
				f=input('파일명을 입력해주세요: ')
				df2.to_csv(f)
				print('저장이 완료되었습니다.')

	if(c==2):
		df2=df1.sort_values(by=['A'],ascending=[False])
		df2=df2.reset_index(drop=True)
		print(df2)
		d=input('위와 같이 정렬된 파일을 저장하시겠습니까?(y/n)')
		if(d=='y'):
			e=input('파일명은 result.csv파일로 저장됩니다. 다른 이름을 원하시면 n을 눌러주세요.(y/n)')
			if(e=='y'):		
				df2.to_csv("result.csv")
				print('저장이 완료되었습니다.')
			if(e=='n'):
				f=input('파일명을 입력해주세요: ')
				df2.to_csv(f)
				print('저장이 완료되었습니다.')

