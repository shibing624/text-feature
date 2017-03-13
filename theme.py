# coding:utf-8
"""
@author:XuMing
"""

from gensim import corpora, models
import ConfigParser
import jieba
import jieba.analyse
import analysis

conf = ConfigParser.ConfigParser()
conf.read("arg.cfg")
stopwords_path = conf.get("path", "stopwords_path")
segmented_path = conf.get("path", "segmented_path")
test_path = conf.get("path", "test_path")
raw_path = conf.get('path', 'raw_path')
result_path = conf.get('path', 'result_path')
topic_num = 20


def get_stopwords_set(file_name):
    with open(file_name, 'r') as f:
        return set([line.strip().decode('utf-8') for line in f])


def get_words_list(file_name, stop_word_file):
    stop_words_set = get_stopwords_set(stop_word_file)
    word_list = []
    with open(file_name, 'r') as f:
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
        result.append(pattern[1][0][0].encode('utf-8'))
    return result


def main():
    files = analysis.get_files(raw_path)
    f_word_result = file(result_path + "/theme_result.txt", "w+")
    f_word_result.write("主题词提取" + "\n")
    for f in files:
        f_word_result.write('\n' + f.split("\\")[-1][:-4].decode('gbk').encode('utf-8') + ":\n")
        topics = extract_theme(f, stopwords_path, 100)
        topic_list = []
        for t in topics:
            if t not in topic_list and len(topic_list) < topic_num:
                topic_list.append(t)
                f_word_result.write(t + '\n')
        print(f + " ok.")
    f_word_result.close()


if __name__ == '__main__':
    main()
