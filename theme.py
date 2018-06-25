# coding:utf-8
"""
@author:XuMing
"""

from gensim import corpora, models
import config
import jieba
import jieba.analyse
import train
from codecs import open

stopwords_path = config.stopwords_path
segmented_path = config.segmented_path
test_path = config.test_path
raw_path = config.raw_path
result_path = config.result_path
topic_num = 20


def get_stopwords_set(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        return set([line.strip() for line in f])


def get_words_list(file_name, stop_word_file):
    stop_words_set = get_stopwords_set(stop_word_file)
    word_list = []
    with open(file_name, 'r', encoding='utf-8') as f:
        for line in f:
            tmp_list = list(jieba.cut(line.strip(), cut_all=False))
            word_list.append([i for i in tmp_list if i not in stop_words_set])
        return word_list


def extract_theme(raw_file, stop_word_file, num_topics=10):
    result = []
    # 列表，每个元素也是列表，即分词后的词语列表
    word_list = get_words_list(raw_file, stop_word_file)
    # 生成文档的词典，每个此与一个整形索引值对应
    word_dict = corpora.Dictionary(word_list)
    # 词频统计，转化为空间向量格式
    corpus_list = [word_dict.doc2bow(text) for text in word_list]
    lda = models.ldamodel.LdaModel(corpus=corpus_list, id2word=word_dict, num_topics=num_topics, alpha='auto')
    for pattern in lda.show_topics(num_topics=num_topics, num_words=1, formatted=False):
        result.append(pattern[1][0][0])
    return result


def main():
    files = train.get_files(raw_path)
    file_name = result_path + "/theme_result.txt"
    f_word_result = open(file_name, "w+", encoding='utf-8')
    f_word_result.write("主题词提取" + "\n")
    for f in files:
        f_word_result.write('\n' + f.split("\\")[-1][:-4] + ":\n")
        topics = extract_theme(f, stopwords_path, 100)
        topic_list = []
        for t in topics:
            if t not in topic_list and len(topic_list) < topic_num:
                topic_list.append(t)
                f_word_result.write(t + '\n')
        print('save to: ' + file_name + " ok.")
    f_word_result.close()


if __name__ == '__main__':
    main()
