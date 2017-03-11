# coding=utf-8
import sys
import time
import os
import ConfigParser
import collections
import jieba
import jieba.analyse
from textrank4zh import TextRank4Keyword, TextRank4Sentence

conf = ConfigParser.ConfigParser()
conf.read("arg.cfg")
stopwords_path = conf.get("path", "stopwords_path")
stopwords = {word.decode("utf-8") for word in open(stopwords_path).read().split()}
a_path = conf.get("path", "a_path")
b_path = conf.get("path", "b_path")
test_path = conf.get("path", "test_path")
raw_path = conf.get('path', 'raw_path')
segmented_path = conf.get('path', 'segmented_path')
top_word_num = 30
top_sentence_num = 10


def analysis_sentence():
    files = getFiles(raw_path)
    for f in files:
        f_word_result = file(f.split("\\")[-1][:-4] + "_sentence_result.txt", "w+")
        content = open(f).read()
        f_word_result.write("\n\n" + "关键词：" + "\n")
        tags = jieba.analyse.extract_tags(content, top_word_num)
        for i in tags:
            f_word_result.write(i.encode('utf-8') + '\n')

        word = TextRank4Keyword()
        word.analyze(content)
        phrase = word.get_keyphrases(keywords_num=top_word_num, min_occur_num=2)
        f_word_result.write("\n\n" + "关键词组：" + "\n")
        for p in phrase:
            f_word_result.write(p.encode('utf-8') + '\n')

        f_word_result.write("\n\n" + "摘要：" + "\n")
        sentence = TextRank4Sentence()
        sentence.analyze(content)
        s_list = sentence.get_key_sentences(num=top_sentence_num)
        for s in s_list:
            f_word_result.write(s.sentence.encode('utf-8') + '\n')
        print(f,' ok ')
        f_word_result.close()


def analysis_word():
    files = getFiles(b_path)
    result_file = file("result.txt", "w+")
    for f in files:
        f_word_result = file(f.split("\\")[-1][:-4] + "_word_result.txt", "w+")
        content = open(f).read().split("  ")

        text_list = [word.decode("utf-8") for word in content]
        text_set = {word.decode("utf-8") for word in content}
        print " ", a_path, " text_list:", len(text_list)
        print len(text_set), "text", len(set(text_set))

        n_list = [w for w in text_list if w.endswith('/n')]
        print len(n_list)  # 名词
        # 利用collections库中的Counter模块，可以很轻松地得到一个由单词和词频组成的字典。
        freq = collections.Counter(n_list)
        print freq
        # 词频前N的单词
        top_freq = freq.most_common(2)
        print top_freq
        n_set = sorted([w for w in text_list if w.endswith('/n')])
        print len(n_set)  # 名词
        result_file.writelines(str(len(n_set)) + " ")
        n_top = collections.Counter(n_set).most_common(100)
        f_word_result.write("\n\n名词:" + "\n")
        write_word(f_word_result, n_top)

        v_set = sorted([w for w in text_list if w.endswith('/v')])
        print len(v_set)  # 动词
        result_file.writelines(str(len(v_set)) + " ")
        v_top = collections.Counter(v_set).most_common(100)
        f_word_result.write("\n\n动词:" + "\n")
        write_word(f_word_result, v_top)

        a_set = sorted([w for w in text_list if w.endswith('/a')])
        print len(a_set)  # 形容词
        result_file.writelines(str(len(a_set)) + " ")
        a_top = collections.Counter(a_set).most_common(100)
        f_word_result.write("\n\n形容词:" + "\n")
        write_word(f_word_result, a_top)

        m_set = sorted([w for w in text_list if w.endswith('/m')])
        print len(m_set)  # 数词
        result_file.writelines(str(len(m_set)) + " ")
        m_top = collections.Counter(m_set).most_common(100)
        f_word_result.write("\n\n数词:" + "\n")
        write_word(f_word_result, m_top)

        r_set = sorted([w for w in text_list if w.endswith('/r')])
        print len(r_set)  # 代词
        result_file.writelines(str(len(r_set)) + " ")
        r_top = collections.Counter(r_set).most_common(100)
        f_word_result.write("\n\n代词:" + "\n")
        write_word(f_word_result, r_top)

        q_set = sorted([w for w in text_list if w.endswith('/q')])
        print len(q_set)  # 量词
        result_file.writelines(str(len(q_set)) + " ")
        q_top = collections.Counter(q_set).most_common(100)
        f_word_result.write("\n\n量词:" + "\n")
        write_word(f_word_result, q_top)

        d_set = sorted([w for w in text_list if w.endswith('/d')])
        print len(d_set)  # 副词
        result_file.writelines(str(len(d_set)) + " ")
        d_top = collections.Counter(d_set).most_common(100)
        f_word_result.write("\n\n副词:" + "\n")
        write_word(f_word_result, d_top)

        p_set = sorted([w for w in text_list if w.endswith('/p')])
        print len(p_set)  # 介词
        result_file.writelines(str(len(p_set)) + " ")
        p_top = collections.Counter(p_set).most_common(100)
        f_word_result.write("\n\n介词:" + "\n")
        write_word(f_word_result, p_top)

        c_set = sorted([w for w in text_list if w.endswith('/c')])
        print len(c_set)  # 连词
        result_file.writelines(str(len(c_set)) + " ")
        c_top = collections.Counter(c_set).most_common(100)
        f_word_result.write("\n\n连词:" + "\n")
        write_word(f_word_result, c_top)

        u_set = sorted([w for w in text_list if w.endswith('/u')])
        print len(u_set)  # 助词
        result_file.writelines(str(len(u_set)) + " ")
        u_top = collections.Counter(u_set).most_common(100)
        f_word_result.write("\n\n助词:" + "\n")
        write_word(f_word_result, u_top)

        e_set = sorted([w for w in text_list if w.endswith('/e')])
        print len(e_set)  # 叹词
        result_file.writelines(str(len(e_set)) + " ")
        e_top = collections.Counter(e_set).most_common(100)
        f_word_result.write("\n\n叹词:" + "\n")
        write_word(f_word_result, e_top)

        o_set = sorted([w for w in text_list if w.endswith('/o')])
        print len(o_set)  # 拟声词
        result_file.writelines(str(len(o_set)) + " ")
        o_top = collections.Counter(o_set).most_common(100)
        f_word_result.write("\n\n拟声词:" + "\n")
        write_word(f_word_result, o_top)

        w_set = sorted([w for w in text_list if w.endswith('/w')])
        print len(w_set)  # 标点
        result_file.writelines("punctuation:" + str(len(w_set)) + " ")
        w_top = collections.Counter(w_set).most_common(100)
        f_word_result.write("\n\n标点:" + "\n")
        write_word(f_word_result, w_top)

        nh_set = sorted([w for w in text_list if '/nh' in w])
        print len(nh_set)  # 人名
        result_file.writelines("person_name:" + str(len(nh_set)) + " ")
        nh_top = collections.Counter(nh_set).most_common(100)
        f_word_result.write("\n\n人名:" + "\n")
        write_word(f_word_result, nh_top)

        result_file.write(str(f) + " word_total_count: " + str(len(text_list)) + "\n")
        f_word_result.close()
    result_file.close()


def getFiles(path):
    list = []
    for parent, dirnames, filenames in os.walk(path):  # 三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
        for filename in filenames:  # 输出文件信息
            # print "parent is:" + parent
            # print "filename is:" + filename
            # print "the full name of the file is:" + os.path.join(parent, filename)  # 输出文件路径信息
            list.append(os.path.join(parent, filename))
        print list
        return list


def write_word(f_word_result, top):
    for i in top:
        for k in i:
            if isinstance(k, int):
                f_word_result.write("\t" + str(k) + "\n")
            else:
                f_word_result.write(k.encode('utf-8').split('/')[0])


if __name__ == '__main__':
    analysis_word()
    analysis_sentence()
