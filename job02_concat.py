import pandas as pd
import glob

data_paths=glob.glob('D:/AI_exam/intel_second_crawling/crawling_data4/*')

print(data_paths[:-5])

df=pd.DataFrame()

for path in data_paths:
    df_temp=pd.read_csv(path)

    df_temp.dropna(inplace=True)
    df_temp.drop_duplicates(inplace=True)

    df=pd.concat([df,df_temp],ignore_index=True)

df.drop_duplicates(inplace=True)

df.info()

my_year=2023

df.to_csv('D:/AI_exam/intel_second_crawling/crawling_data4/reviews_{}.csv'.format(my_year),index=False)









