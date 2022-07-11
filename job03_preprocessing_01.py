import pandas as pd
from konlpy.tag import Okt
import re

df = pd.read_csv('./crawling_data/reviews_2019.csv')
df.info()

okt = Okt()

df_stopwords = pd.read_csv('./crawling_data/stopwords.csv')
stopwords = list(df_stopwords['stopword'])
stopwords =stopwords+['영화','연출','관객','개봉','개봉일','주인공',
                      '출연','배우','리뷰','극장','장면','관람','연기',
                      '되어다',]
count=0
cleaned_sentences = []
for review in df.reviews:
    count+=1
    review = re.sub('[^가-힣 ]', ' ', review)

    ##2019년도만 사용
    review=review.split()
    words=[]
    for word in review:
        if len(word)>20:
            word=' '
        words.append(word)
    review=' '.join(words)
    ##

    token = okt.pos(review, stem=True)

    df_token = pd.DataFrame(token, columns=['word', 'class'])
    df_token = df_token[(df_token['class'] == 'Noun') |
                        (df_token['class'] == 'Verb') |
                        (df_token['class'] == 'Adjective')]
    words = []
    for word in df_token.word:
        if 1< len(word) < 20:
            if word not in stopwords:
                words.append(word)
    cleaned_sentence = ' '.join(words)
    cleaned_sentences.append(cleaned_sentence)
    print(words)
    print(count)

df['cleaned_sentences'] = cleaned_sentences
df = df[['title', 'cleaned_sentences']]
df.dropna(inplace=True)

df.to_csv('./crawling_data/cleaned_review_2019.csv', index=False)
df.info()