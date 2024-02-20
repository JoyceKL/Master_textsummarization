from scipy.linalg import svd
from nltk.cluster.util import cosine_distance
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

def build_similarity_matrix(sentences, stopwords=None):
    vectorizer = TfidfVectorizer(stop_words=stopwords)
    tfidf_matrix = vectorizer.fit_transform(sentences)

    U, s, Vt = svd(tfidf_matrix.toarray())

    sm = np.zeros([len(sentences), len(sentences)])

    for i in range(len(sentences)):
        for j in range(len(sentences)):
            sm[i][j] = 1 - cosine_distance(U[i], U[j])

    return sm
