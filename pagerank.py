import numpy as np

np.seterr(divide='ignore', invalid='ignore')

from similarity_matrix import build_similarity_matrix

option1 = 20
option2 = 42


class TextRank:
    def __init__(self):
        self.damping = 0.85  # Hệ số suy giảm (0.85)
        self.min_diff = 1e-5  # Ngưỡng hội tụ
        self.steps = 100  # Số bước lặp
        self.text_str = None
        self.sentences = None
        self.pr_vector = None

    def run_page_rank(self, similarity_matrix):

        pr_vector = np.array([1] * len(similarity_matrix))

        previous_pr = 0

        # Lặp
        for epoch in range(self.steps):
            pr_vector = (1 - self.damping) + self.damping * np.matmul(similarity_matrix, pr_vector)
            if abs(previous_pr - sum(pr_vector)) < self.min_diff:
                break
            else:
                previous_pr = sum(pr_vector)

        return pr_vector

    def get_result(self, listSentences, option):
        if option == 1:
            number = option1
        else:
            number = option2

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

    def analyze(self, listSentences, stop_words=None):
        text_str = []
        for value in listSentences:
            text_str.append(value.textvalue)

        similarity_matrix = build_similarity_matrix(text_str, stop_words)

        self.pr_vector = self.run_page_rank(similarity_matrix)
