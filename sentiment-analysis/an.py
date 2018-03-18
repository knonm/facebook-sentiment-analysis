import nltk
import re
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
from sklearn.model_selection import cross_val_predict

def PreprocessamentoSemStopWords(instancia):
    #remove links dos tweets
    #remove stopwords
    instancia = re.sub(r"[@#]\S*", "", instancia)
    instancia = re.sub(r"http\S+", "", instancia).lower().replace(',','').replace('.','').replace(';','').replace('-','')
    instancia = re.sub(r"[^\w\s]+", "", instancia)
    # instancia = re.sub(r"http\S+", "", instancia).lower().replace(',','').replace('.','').replace(';','').replace('-','')
    stopwords = set(nltk.corpus.stopwords.words('portuguese'))
    palavras = [i for i in instancia.split() if not i in stopwords]
    return (" ".join(palavras))

def Stemming(instancia):
    stemmer = nltk.stem.RSLPStemmer()
    palavras=[]
    for w in instancia.split():
        palavras.append(stemmer.stem(w))
    return (" ".join(palavras))

dataset = pd.read_csv('/home/knonm/Desktop/Tweets_Mg.csv',encoding='utf-8')

dataset.count()
dataset[dataset.Classificacao=='Neutro'].count()
dataset[dataset.Classificacao=='Positivo'].count()
dataset[dataset.Classificacao=='Negativo'].count()

PreprocessamentoSemStopWords('Eu não gosto do partido, e também não votaria novamente nesse governante!')

tweets = dataset['Text'].values

tweets2 = []
for t in tweets:
    tmp = t
    tweets2.append(PreprocessamentoSemStopWords(tmp))

classes = dataset['Classificacao'].values

vectorizer = CountVectorizer(analyzer="word")
freq_tweets = vectorizer.fit_transform(tweets2)

modelo = MultinomialNB()
modelo.fit(freq_tweets,classes)
