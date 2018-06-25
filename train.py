# coding=utf-8
from __future__ import division

import collections
import os

import config
from codecs import open
stopwords_path = config.stopwords_path
segmented_path = config.segmented_path
sentence_symbol_path = config.sentence_symbol_path
test_path = config.test_path
raw_path = config.raw_path
result_path = config.result_path


def analysis_word(path=segmented_path):
    result_file_path = result_path + '/word_result.txt'
    files = get_files(path)
    result_file = open(result_file_path, "w+", encoding='utf-8')
    result_file.writelines(
        "文件名" + "\t" + "名词数" + "\t" + "名词数占比" + "\t" + "动词数" + "\t" + "动词数占比" + "\t" + "形容词数" + "\t" +
        "形容词数占比" + "\t" + "数词数" + "\t" + "数词数占比" + "\t" + "代词数" + "\t" + "代词数占比" + "\t" +
        "量词数" + "\t" + "量词数占比" + "\t" + "副词数" + "\t" + "副词数占比" + "\t" + "介词数" + "\t" + "介词数占比" + "\t" +
        "连词数" + "\t" + "连词数占比" + "\t" + "助词数" + "\t" + "助词数占比" + "\t" + "叹词数" + "\t" + "叹词数占比" + "\t" +
        "拟声词数" + "\t" + "拟声词数占比" + "\t" + "标点数" + "\t" + "标点数占比" + "\t" + "人名数" + "\t" + "人名数占比" + "\t" +
        "词总数" + "\t" + "字总数" + "\t" + "平均词长" + "\t" + "一字词数" + "\t" + "一字词占比" + "\t" +
        "二字词数" + "\t" + "二字词占比" + "\t" + "三字词数" + "\t" + "三字词占比" + "\t" + "四字词数" + "\t" +
        "四字词占比" + "\t" + "段落数" + "\t" + "段落平均字数" + "\t" +
        "句子数（长句）" + "\t" + "句子平均字数（长句）" + "\t" + "句子数（短句）" + "\t" + "句子平均字数（短句）" + "\t""\n")
    for f in files:
        f_word_result = open(result_path + '/' + f.split('/')[-1][:-4] + "_word_result.txt", "w+", encoding='utf-8')
        c = open(f,encoding='utf-8').read()
        print('paragraphs:', c.count('\n'))
        num_paragraph = c.count('\n')
        print('num_word:', len(c.split()))
        content_list = c.split()
        text_list = [word for word in content_list]
        print(" ", path, " text_list:", len(text_list))

        n_list = [w for w in text_list if w.endswith('/n')]
        print(len(n_list))  # 名词
        # 利用collections库中的Counter模块，可以很轻松地得到一个由单词和词频组成的字典。
        freq = collections.Counter(n_list)
        print(freq)
        # 词频前N的单词
        top_freq = freq.most_common(2)
        print(top_freq)

        # 文件名称
        result_file.write('' + f.split("/")[-1][:-4] + "\t")
        num_word = len(text_list)  # 词总数
        n_set = sorted([w for w in text_list if w.endswith('/n')])
        print(len(n_set))  # 名词
        result_file.writelines(str(len(n_set)) + "\t")
        result_file.write(str(float(len(n_set) / num_word)) + "\t")
        n_top = collections.Counter(n_set).most_common(100)
        f_word_result.write("名词:" + "\n")
        write_word(f_word_result, n_top)

        v_set = sorted([w for w in text_list if w.endswith('/v')])
        print(len(v_set))  # 动词
        result_file.writelines(str(len(v_set)) + "\t")
        result_file.write(str(float(len(v_set) / num_word)) + "\t")
        v_top = collections.Counter(v_set).most_common(100)
        f_word_result.write("\n\n动词:" + "\n")
        write_word(f_word_result, v_top)

        a_set = sorted([w for w in text_list if w.endswith('/a')])
        print(len(a_set))  # 形容词
        result_file.writelines(str(len(a_set)) + "\t")
        result_file.write(str(float(len(a_set) / num_word)) + "\t")
        a_top = collections.Counter(a_set).most_common(100)
        f_word_result.write("\n\n形容词:" + "\n")
        write_word(f_word_result, a_top)

        m_set = sorted([w for w in text_list if w.endswith('/m')])
        print(len(m_set))  # 数词
        result_file.writelines(str(len(m_set)) + "\t")
        result_file.write(str(float(len(m_set) / num_word)) + "\t")
        m_top = collections.Counter(m_set).most_common(100)
        f_word_result.write("\n\n数词:" + "\n")
        write_word(f_word_result, m_top)

        r_set = sorted([w for w in text_list if w.endswith('/r')])
        print(len(r_set))  # 代词
        result_file.writelines(str(len(r_set)) + "\t")
        result_file.write(str(float(len(r_set) / num_word)) + "\t")
        r_top = collections.Counter(r_set).most_common(100)
        f_word_result.write("\n\n代词:" + "\n")
        write_word(f_word_result, r_top)

        q_set = sorted([w for w in text_list if w.endswith('/q')])
        print(len(q_set))  # 量词
        result_file.writelines(str(len(q_set)) + "\t")
        result_file.write(str(float(len(q_set) / num_word)) + "\t")
        q_top = collections.Counter(q_set).most_common(100)
        f_word_result.write("\n\n量词:" + "\n")
        write_word(f_word_result, q_top)

        d_set = sorted([w for w in text_list if w.endswith('/d')])
        print(len(d_set))  # 副词
        result_file.writelines(str(len(d_set)) + "\t")
        result_file.write(str(float(len(d_set) / num_word)) + "\t")
        d_top = collections.Counter(d_set).most_common(100)
        f_word_result.write("\n\n副词:" + "\n")
        write_word(f_word_result, d_top)

        p_set = sorted([w for w in text_list if w.endswith('/p')])
        print(len(p_set))  # 介词
        result_file.writelines(str(len(p_set)) + "\t")
        result_file.write(str(float(len(p_set) / num_word)) + "\t")
        p_top = collections.Counter(p_set).most_common(100)
        f_word_result.write("\n\n介词:" + "\n")
        write_word(f_word_result, p_top)

        c_set = sorted([w for w in text_list if w.endswith('/c')])
        print(len(c_set))  # 连词
        result_file.writelines(str(len(c_set)) + "\t")
        result_file.write(str(float(len(c_set) / num_word)) + "\t")
        c_top = collections.Counter(c_set).most_common(100)
        f_word_result.write("\n\n连词:" + "\n")
        write_word(f_word_result, c_top)

        u_set = sorted([w for w in text_list if w.endswith('/u')])
        print(len(u_set))  # 助词
        result_file.writelines(str(len(u_set)) + "\t")
        result_file.write(str(float(len(u_set) / num_word)) + "\t")
        u_top = collections.Counter(u_set).most_common(100)
        f_word_result.write("\n\n助词:" + "\n")
        write_word(f_word_result, u_top)

        e_set = sorted([w for w in text_list if w.endswith('/e')])
        print(len(e_set))  # 叹词
        result_file.writelines(str(len(e_set)) + "\t")
        result_file.write(str(float(len(e_set) / num_word)) + "\t")
        e_top = collections.Counter(e_set).most_common(100)
        f_word_result.write("\n\n叹词:" + "\n")
        write_word(f_word_result, e_top)

        o_set = sorted([w for w in text_list if w.endswith('/o')])
        print(len(o_set))  # 拟声词
        result_file.writelines(str(len(o_set)) + "\t")
        result_file.write(str(float(len(o_set) / num_word)) + "\t")
        o_top = collections.Counter(o_set).most_common(100)
        f_word_result.write("\n\n拟声词:" + "\n")
        write_word(f_word_result, o_top)

        w_set = sorted([w for w in text_list if w.endswith('/w')])
        print(len(w_set))  # 标点
        result_file.writelines(str(len(w_set)) + "\t")
        result_file.write(str(float(len(w_set) / num_word)) + "\t")
        w_top = collections.Counter(w_set).most_common(100)
        f_word_result.write("\n\n标点:" + "\n")
        write_word(f_word_result, w_top)

        nh_set = sorted([w for w in text_list if '/nh' in w])
        print(len(nh_set))  # 人名
        result_file.writelines(str(len(nh_set)) + "\t")
        result_file.write(str(float(len(nh_set) / num_word)) + "\t")
        nh_top = collections.Counter(nh_set).most_common(100)
        f_word_result.write("\n\n人名:" + "\n")
        write_word(f_word_result, nh_top)

        result_file.write(str(num_word) + "\t")  # 词总数
        word_list = [w.split('/')[0] for w in text_list]
        sentence_symbol = [word for word in open(sentence_symbol_path,encoding='utf-8').read().split()]
        sentence_list_long = [w for w in word_list if w in sentence_symbol[:6]]  # 长句
        sentence_list_short = [w for w in word_list if w in sentence_symbol]  # 短句
        num_sentence_long = len(sentence_list_long)  # 段落数
        num_sentence_short = len(sentence_list_short)  # 段落数
        word_no_pos_len_list = [len(w.split('/')[0]) for w in text_list]

        num_char = sum(len(w.split('/')[0]) for w in text_list)  # 字总数
        result_file.write(str(num_char) + "\t")  # 字总数
        average_word_len = float(num_char / num_word)
        print("word average length: ", str(average_word_len))
        result_file.write(str(average_word_len) + "\t")  # 单词平均长度

        # 利用collections库中的Counter模块，可以很轻松地得到一个由单词和词频组成的字典。
        len_counts = collections.Counter(word_no_pos_len_list)
        if len_counts.get(1):
            result_file.write(str(len_counts.get(1)) + "\t")  # 1字词个数
            result_file.write(str(float(len_counts.get(1) / num_word)) + "\t")  # 1字词占比
        else:
            result_file.write(str(0) + "\t" + str(0) + "\t")
        if len_counts.get(2):
            result_file.write(str(len_counts.get(2)) + "\t")  # 2字词个数
            result_file.write(str(float(len_counts.get(2) / num_word)) + "\t")  # 2字词占比
        else:
            result_file.write(str(0) + "\t" + str(0) + "\t")
        if len_counts.get(3):
            result_file.write(str(len_counts.get(3)) + "\t")  # 3字词个数
            result_file.write(str(float(len_counts.get(3) / num_word)) + "\t")  # 3字词占比
        else:
            result_file.write(str(0) + "\t" + str(0) + "\t")
        if len_counts.get(4):
            result_file.write(str(len_counts.get(4)) + "\t")  # 4字词个数
            result_file.write(str(float(len_counts.get(4) / num_word)) + "\t")  # 4字词占比
        else:
            result_file.write(str(0) + "\t" + str(0) + "\t")
        if num_paragraph > 0:
            result_file.write(str(num_paragraph) + "\t")  # 段落数
            result_file.write(str(float(num_char / num_paragraph)) + "\t")  # 段落平均字数
        else:
            result_file.write(str(0) + "\t" + str(0) + "\t")
        if num_sentence_long > 0:
            result_file.write(str(num_sentence_long) + "\t")  # 句子数（长句）
            result_file.write(str(float(num_char / num_sentence_long)) + "\t")  # 句子平均字数
        else:
            result_file.write(str(0) + "\t" + str(0) + "\t")
        if num_sentence_short > 0:
            result_file.write(str(num_sentence_short) + "\t")  # 句子数(短句)
            result_file.write(str(float(num_char / num_sentence_short)) + "\t")  # 句子平均字数（短句）
        else:
            result_file.write(str(0) + "\t" + str(0) + "\t")
        result_file.write("\n")
        f_word_result.close()
    result_file.close()


def get_files(path):
    files = []
    for parent, dirnames, filenames in os.walk(path):  # 三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
        for filename in filenames:  # 输出文件信息
            # print("parent is:" + parent
            # print("filename is:" + filename
            # print("the full name of the file is:" + os.path.join(parent, filename)  # 输出文件路径信息
            files.append(os.path.join(parent, filename))
        return files


def write_word(f_word_result, tops):
    for top in tops:
        f_word_result.write(top[0].split('/')[0] + "\t")
        f_word_result.write(str(top[1]))
        f_word_result.write("\n")


if __name__ == '__main__':
    analysis_word()
