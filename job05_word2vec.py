import pandas as pd
from gensim.models import Word2Vec

review_word=pd.read_csv('./crawling_data/reviews_2017_2022.csv')
review_word.info()

cleaned_token_reviews=list(review_word['reviews'])
print(cleaned_token_reviews[0])

cleaned_tokens=[]
for sentence in cleaned_token_reviews:
    token=sentence.split()
    cleaned_tokens.append(token)
print(cleaned_tokens[0])
embedding_model=Word2Vec(cleaned_tokens,vector_size=100,   #size:차원=100
                         window=4,min_count=20,     #windows:4개씩 끊어 학습
                         workers=4,epochs=100,sg=1) #min_count:최소20번 빈도나온 단어를 벡터라이징

embedding_model.save('./models/word2vec_2017_2022_movies.model')
print(list(embedding_model.wv.index_to_key))
print(len(embedding_model.wv.index_to_key))