import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer

from scipy.io import mmwrite,mmread

import pickle

df_reviews=pd.read_csv('D:/AI_exam/intel_second_crawling/crawling_data4/cleaned_one_review.csv')

df_reviews.info()

Tfidf=TfidfVectorizer(sublinear_tf=True)

Tfidf_matrix=Tfidf.fit_transform(df_reviews['reviews'])

print(Tfidf_matrix.shape)

with open('D:/AI_exam/intel_second_crawling/models/tfidf.pickle','wb') as f:
    pickle.dump(Tfidf,f)

mmwrite('D:/AI_exam/intel_second_crawling/models/Tfidf_movie_review.mtx',Tfidf_matrix)






