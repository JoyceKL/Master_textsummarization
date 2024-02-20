import numpy as np
from scipy.linalg import svd

np.seterr(divide='ignore', invalid='ignore')

from similarity_matrix import build_similarity_matrix

class TextRank:
    def __init__(self):
        self.damping = 0.85  # Hệ số suy giảm (0.85)
        self.min_diff = 1e-5  # Ngưỡng hội tụ
        self.steps = 100  # Số bước lặp
        self.text_str = None
        self.sentences = None
        self.pr_vector = None

    def run_page_rank(self, similarity_matrix, damping=0.85, max_iterations=100, epsilon=1e-5):
        n = similarity_matrix.shape[0]
        page_rank = np.ones(n) / n  # Khởi tạo vector PageRank

        for _ in range(max_iterations):
            new_page_rank = np.ones(n) * (1 - damping) / n + damping * np.dot(similarity_matrix.T, page_rank)

            # Kiểm tra điều kiện dừng
            if np.linalg.norm(new_page_rank - page_rank, ord=1) <= epsilon:
                return new_page_rank

            page_rank = new_page_rank

        return page_rank  # Trả về vector PageRank sau khi hội tụ
    def get_result(self, listSentences, U, option):
        if option == 1:
            number = 1
        else:
            number = 2

        top_sentences = []
        try:
            if self.pr_vector is not None:
                sorted_pr = np.argsort(self.pr_vector)
                sorted_pr = list(sorted_pr)
                sorted_pr.reverse()

                index = 0
                for epoch in range(number):
                    sent = listSentences[sorted_pr[index]]
                    top_sentences.append(sent)
                    index += 1
            return top_sentences

        except Exception as e:
            pass
    # def analyze(self, sentences, stop_words):
    #     text_str = [sentence.textvalue for sentence in sentences]
    #     similarity_matrix = build_similarity_matrix(text_str, stop_words)  
    #     self.run_page_rank(similarity_matrix)
    #     return similarity_matrix
    # Trong phương thức analyze của lớp TextRank
    def analyze(self, sentences, stop_words):
        text_str = [sentence.textvalue for sentence in sentences]
        similarity_matrix = build_similarity_matrix(text_str, stop_words)  
        print("Similarity Matrix:")
        print(similarity_matrix)  # Debug và in ra ma trận tương đồng
        self.run_page_rank(similarity_matrix)
        print("PageRank Vector:")
        print(self.pr_vector)  # Debug và in ra vector PageRank
        return similarity_matrix


