import os
from bs4 import BeautifulSoup as Soup
from nltk.corpus import stopwords as st
from collections import Counter
import glob

from pagerank import TextRank


# Lọc List bỏ các Tag trừ <s>
def filter_list_tag(textfiles):
    filter_files = []
    for text in textfiles:
        if "P>" in text:
            continue
        elif "TEXT>" in text:
            continue
        elif "SUBJECT>" in text:
            continue
        elif "TYPE>" in text:
            continue
        elif "GRAPHIC>" in text:
            continue
        elif "XX>" in text:
            continue
        elif "CO>" in text:
            continue
        elif "CN>" in text:
            continue
        elif "IN>" in text:
            continue
        elif "PUB>" in text:
            continue
        elif "PAGE>" in text:
            continue
        elif "HEAD>" in text:
            continue
        elif "BYLINE>" in text:
            continue
        elif "COUNTRY>" in text:
            continue
        elif "CITY>" in text:
            continue
        elif "EDITION>" in text:
            continue
        elif "CODE>" in text:
            continue
        elif "NAME>" in text:
            continue
        elif "PUBDATE>" in text:
            continue
        elif "DAY>" in text:
            continue
        elif "MONTH>" in text:
            continue
        elif "PG.COL>" in text:
            continue
        elif "PUBYEAR>" in text:
            continue
        elif "REGION>" in text:
            continue
        elif "FEATURE>" in text:
            continue
        elif "STATE>" in text:
            continue
        elif "WORD.CT>" in text:
            continue
        elif "DATELINE>" in text:
            continue
        elif "COPYRGHT>" in text:
            continue
        elif "LIMLEN>" in text:
            continue
        elif "LANGUAGE>" in text:
            continue
        elif "NOTE>" in text:
            continue
        elif "TABLE>" in text:
            continue
        elif "ROWRULE>" in text:
            continue
        elif "TABLEROW>" in text:
            continue
        elif "CELLRULE>" in text:
            continue
        elif "TABLECELL>" in text:
            continue
        elif "F>" in text:
            continue
        filter_files.append(text)
    return filter_files


class TextClass:
    def __init__(self, docid, num, wdcount, textvalue):
        self.docid = docid
        self.num = num
        self.wdcount = wdcount
        self.textvalue = textvalue

    @staticmethod
    def readfile():
        list_of_files = glob.glob('DUC_TEXT/*')
        list_of_files.sort()

        for file_name in list_of_files:
            f = open(file_name, 'r')
            pagetext = f.readlines()
            filtertext = filter_list_tag(pagetext)
            lst = []

            tr4sh = TextRank()

            print("====================OPEN FILE" + file_name + "====================")

            listSentences = []

            for sentences in filtertext:
                getText = Soup(sentences, 'xml')
                sentence = TextClass(getText.s['docid'], getText.s['num'], getText.s['wdcount'],
                                     getText.s.string.strip())
                listSentences.append(sentence)
            print("====================HANDING FILE====================")
            tr4sh.analyze(listSentences, st.words('english'))
            res = tr4sh.get_result(listSentences, 1)

            f.close()

            print("====================WRITE FILE " + file_name.replace("DUC_TEXT/", "") + "====================")
            # Tạo thư mục nếu chưa tồn tại
            output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'DUC_RES', 'WAY_1')
            os.makedirs(output_dir, exist_ok=True)


            # Mở tệp tin để ghi
            fs = open(os.path.join(output_dir, os.path.basename(file_name)), 'w')


            for item in res:
                fs.write(item.textvalue + '\n')

            fs.close()

            f = open(file_name.replace("DUC_TEXT/", "DUC_SUM/"), 'r')
            text_sum = f.readlines()
            filtered_sum = filter_list_tag(text_sum)

            list_sentences_sum = []

            for sentences_sum in filtered_sum:
                get_text_sum = Soup(sentences_sum, 'xml')
                sentence_sum = TextClass(get_text_sum.s['docid'], get_text_sum.s['num'], get_text_sum.s['wdcount'],
                                         get_text_sum.s.string.strip())
                list_sentences_sum.append(sentence_sum)

            print("Tổng câu: " + str(len(listSentences)))
            resatt = (o.textvalue for o in res)
            sumatt = (o.textvalue for o in list_sentences_sum)

            cnt_dct = len(set(resatt) & set(sumatt))

            print("Số câu lấy trùng: " + str(cnt_dct) + "/" + str(len(list_sentences_sum)))
            print("Tỉ lệ " + str(round((cnt_dct / len(list_sentences_sum)), 2) * 100))
