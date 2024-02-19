from scipy.spatial.distance import cosine
from nltk.cluster.util import cosine_distance
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

def get_symmetric_matrix(matrix):
    """
    Lấy ma trận đối xứng
    :param matrix:
    :return: matrix
    """
    return matrix + matrix.T - np.diag(matrix.diagonal())


# Loại bỏ ký tự thừa trong câu
def cleartext(item_str):
    last_index = 0
    if item_str.endswith("."):
        last_index = item_str.index(".")
    elif item_str.endswith("'"):
        last_index = item_str.index("'")
    item_remove = item_str[0:last_index]
    item_convert = ""
    item_splits = item_remove.split(" ")
    for item_split in item_splits:
        if item_split.endswith(","):
            item_split = item_split[0:item_split.index(",")]
        elif item_split.endswith("''"):
            item_split = item_split[0:item_split.index("''")]
        elif item_split.startswith("''"):
            item_split = item_split[0:item_split.index("''")]
        elif item_split.startswith("``"):
            item_split = item_split[0:item_split.index("``")]
        item_convert += item_split + " "
    return item_convert


def sentence_count(sent1, sent2, stopwords=None, stopnum=None):
    if stopwords is None:
        stopwords = []
    sent1s = cleartext(sent1)
    sent2s = cleartext(sent2)
    sent1 = sent1s.split()
    sent2 = sent2s.split()

    count = list(set(sent1) & set(sent2))
    if len(count) > stopnum:
        return 1
    else:
        return 0


def sentence_similarity(sent1, sent2, stopwords=None):
    if stopwords is None:
        stopwords = []
    sent1s = cleartext(sent1)
    sent2s = cleartext(sent2)
    sent1 = sent1s.split()
    sent2 = sent2s.split()

    # Dùng set để loại bỏ phần tử trùng của 2 câu
    all_words = list(set(sent1 + sent2))

    vector1 = [0] * len(all_words)
    vector2 = [0] * len(all_words)

    # Tạo vector cho từ câu 1
    for w in sent1:
        if w.lower() in stopwords:
            continue
        vector1[all_words.index(w)] += 1

    # Tạo vector cho từ câu 2
    for w in sent2:
        if w.lower() in stopwords:
            continue
        vector2[all_words.index(w)] += 1

    """ 
    print("COSSIM")
    print("vector 1:" + str(vector1))
    print("Sen 1:" + sent1s)
    print("vector 2:" + str(vector2))
    print("Sen 2:" + sent2s)
    print("---")
    """
    # Trả về hàm tính CosSim của 2 vector
    return cal_cossim(vector1, vector2)


# def cal_cossim(vector1, vector2):
#     """
#     Độ đo tương đồng (CosSim) của 2 vector
#     :param vector1:
#     :param vector2:
#     :return: 0 < CosSim value < 1
#     """
#    # print("CosSim:" + str(1 - cosine_distance(vector1, vector2)))
#     return 1 - cosine_distance(vector1, vector2)

def cosine_distance(u, v):
    """
    Tính toán khoảng cách cosine giữa hai vector.
    :param u: Vector 1
    :param v: Vector 2
    :return: Khoảng cách cosine
    """
    return cosine(u, v)

def build_similarity_matrix(sentences, stopwords=None):
    # # Tạo ma trận rỗng
    # sm = np.zeros([len(sentences), len(sentences)])

    # for idx1 in range(len(sentences)):
    #     for idx2 in range(len(sentences)):
    #         if idx1 == idx2:
    #             continue
    #         #Cách 1:
    #         sm[idx1][idx2] = sentence_count(sentences[idx1], sentences[idx2], stopwords=stopwords, stopnum=3)

    #         # Cách 2:
    #         #sm[idx1][idx2] = sentence_similarity(sentences[idx1], sentences[idx2], stopwords=stopwords)
     # Sử dụng TF-IDF Vectorizer để biểu diễn văn bản
    vectorizer = TfidfVectorizer(stop_words=stopwords)
    tfidf_matrix = vectorizer.fit_transform(sentences)

    # Lấy ma trận tương đồng dựa trên cosine similarity
    similarity_matrix = np.zeros((len(sentences), len(sentences)))
    for i in range(len(sentences)):
        for j in range(len(sentences)):
            if i != j:
                similarity_matrix[i][j] = 1 - cosine_distance(tfidf_matrix[i].toarray(), tfidf_matrix[j].toarray())


    similarity_matrix = get_symmetric_matrix(similarity_matrix)

    return similarity_matrix
    # # Lấy ma trận đối xứng
    # sm = get_symmetric_matrix(sm)

    # return sm
