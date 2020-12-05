import pandas as pd

#2번 크롤러를 선택했을 때 기본값이 최신순 정렬인데 이를 오래된 순으로 정렬
df1=pd.read_csv('Article_10_문화일보.csv', names=['A','B','C','D'])
print(df1)
df2=df1.sort_values(by=['D'])
df2=df2.reset_index(drop=True)
print(df2)
df2.to_csv("result.csv")


#1번 크롤러를 선택했을 때 기본값이 오래된 순 정렬인데 이를 최신순으로 정렬

df1=pd.read_csv('Article_오피니언_202009_202009.csv', names=['A','B','C','D','E','F'])
print(df1)
df2=df1.sort_values(by=['A'],ascending=[False])
df2=df2.reset_index(drop=True)
print(df2)
df2.to_csv("result.csv")
