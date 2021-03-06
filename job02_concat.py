import pandas as pd
import glob

'''
df=pd.read_csv('./crawling_data/m2020/reviews_2020_1page.csv')
for i in range(1,38):
    df_temp=pd.read_csv('./crawling_data/m2020/reviews_2020_{}page.csv'.format(i))
    df_temp.dropna(inplace=True)
    df_temp.drop_duplicates(inplace=True)
    df=pd.concat([df,df_temp],ignore_index=True)
df.drop_duplicates(inplace=True)
df.info()
my_year=2020
df.to_csv('./crawling_data/m2020/reviews_{}.csv'.format(my_year),index=False)
'''


df=pd.DataFrame()
data_paths=glob.glob('./crawling_data/CRO/*')
for path in data_paths:
    df_temp=pd.read_csv(path)
    df_temp.dropna(inplace=True)
    df_temp.drop_duplicates(inplace=True)
    df=pd.concat([df,df_temp],ignore_index=True)
df.drop_duplicates(inplace=True)
df.info()
my_year=2020
df.to_csv('./crawling_data/reviews_2017_2022.csv',index=False)
