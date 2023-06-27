import string
from os import path

import spacy
import pandas as pd
from spacy.lang.en import stop_words
from sklearn.feature_extraction.text import TfidfVectorizer

from utils import getMovieName, getReviewFileName

def removePunctuationFromWord(word, punctuation):
    ww = word
    for ch in punctuation:
        ww = ww.replace(ch, '')
    # if len(ww) != len(word):
    #     print(ww, word)
    return ww

if __name__=="__main__":

    sources = ['RogerEbert', 'HollywoodReporter', 'EmpireOnline', 'RollingStone']

    nlp = spacy.load('en_core_web_sm')

    stop = stop_words.STOP_WORDS
    punctuation = string.punctuation + '—' + '’'

    movieWords = dict()
    bagWords = list()

    with open('movies.dat', 'r') as file:

        count = 0
        for row in file:
            movie = getMovieName(row)
            if count >= 100:
                break

            reviews = ''
            for src in sources:
                fileName = getReviewFileName(src, movie)
                if not path.exists(fileName):
                    continue

                with open(fileName, 'r') as file:
                    reviews += file.read() + ' '

            count += 1
            tokens = [token.lemma_.lower().replace(' ', '').replace('\n', '') for token in nlp(reviews)]
            words = [removePunctuationFromWord(t, punctuation) for t in tokens if t not in stop and t not in punctuation and len(t) > 2 and '\n' not in t and not t.isnumeric()]

            movieWords[movie] = words
            bagWords += words
            # print(words)

    # print(bagWords)
    # print(len(bagWords))

    vectorizer = TfidfVectorizer(
        analyzer='word',
        stop_words='english',
        strip_accents='ascii',
        max_features=100)

    vectorizer.fit(bagWords)

    data = vectorizer.transform([' '.join(v) for (k, v) in movieWords.items()])

    tfidf_tokens = vectorizer.get_feature_names_out()

    df = pd.DataFrame(data=data.toarray(), index=[k for (k, v) in movieWords.items()], columns=tfidf_tokens)

    # print(df.head())

    max_df = df.to_dict(orient='index')

    def findMaxScores(features, n=10):
        scores = list()
        for _ in range(n):
            max_key = max(features, key=features.get)
            scores.append(max_key)
            features.pop(max_key)
        return scores

    for (mov, feat) in max_df.items():
        print(mov)
        print(findMaxScores(feat))
        print()

    #for t in tfidf_tokens:
    #    print(t)

