import pandas as pd

from gensim.models import Word2Vec

df_review=pd.read_csv('D:/AI_exam/intel_second_crawling/crawling_data4/cleaned_one_review.csv')

df_review.info()

reviews=list(df_review['reviews'])


print(reviews[0])

tokens=[]

for sentence in reviews:
    token=sentence.split()
    tokens.append(token)

print(tokens[0])

embedding_model=Word2Vec(tokens,vector_size=100,window=4,min_count=20,workers=10,epochs=100,sg=1)












