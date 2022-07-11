import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
from scipy.io import mmread
import pickle
from konlpy.tag import Okt
import re
from gensim.models import Word2Vec

def getRecommendation(cosin_sim):
    simScore=list(enumerate(cosin_sim[-1]))
    simScore=sorted(simScore,key=lambda x:x[1],reverse=True)
    simScore=simScore[:11] #0 자기자신
    movie_index=[i[0] for i in simScore]
    recMovieList=df_reviews.iloc[movie_index,0]
    return recMovieList

df_reviews = pd.read_csv('./crawling_data/reviews_2017_2022.csv')
Tfidf_matrix=mmread('./models/Tfidf_movie_review.mtx').tocsr()
with open('./models/tfidf.pickle','rb')as f:
    Tfidf=pickle.load(f)


'''
#영화제목
movie_idx=df_reviews[df_reviews['titles']=='범죄도시 (THE OUTLAWS)'].index[0]
print(movie_idx)
print(df_reviews.iloc[1228,1])

cosine_sim=linear_kernel(Tfidf_matrix[movie_idx],Tfidf_matrix)
recommendation=getRecommendation(cosine_sim)
print(recommendation[1:11])
'''

'''
#keyword
embedding_model=Word2Vec.load('./models/word2vec_2017_2022_movies.model')
keyword='스파이더맨' ##
sim_word=embedding_model.wv.most_similar(keyword,topn=10)
words=[keyword]
for word,_ in sim_word:
    words.append(word)
sentence=[]
count=10
for word in words:
    sentence=sentence+[word]*count
    count-=1
sentence=' '.join(sentence)
sentence_vec=Tfidf.transform([sentence])
cosine_sim=linear_kernel(sentence_vec,Tfidf_matrix)
recommendation=getRecommendation(cosine_sim)
print(recommendation)
'''

# 문장이용
okt=Okt()
sentence=''    ##
review = re.sub('[^가-힣 ]', ' ', sentence)

token = okt.pos(review, stem=True)

df_token = pd.DataFrame(token, columns=['word', 'class'])
df_token = df_token[(df_token['class'] == 'Noun') |
                    (df_token['class'] == 'Verb') |
                    (df_token['class'] == 'Adjective')]

words = []
for word in df_token.word:
    if 1< len(word) < 20:
        words.append(word)
cleaned_sentence = ' '.join(words)
print(cleaned_sentence)

sentence_vec=Tfidf.transform([sentence])
cosine_sim=linear_kernel(sentence_vec,Tfidf_matrix)
recommendation=getRecommendation(cosine_sim)
print(recommendation)