# -*- coding: utf-8 -*-
# @Time    : 2020/3/30 19:01
# @Author  : lixuedong
# @Email   : 15613316847@163.com
# @File    : mk_freq_dict.py
# @Software: PyCharm
# 1.读取文本文件,支持多文件。
# 2.对每句话进行分词，去除停用词，分词结果添加到词典中。
# 3.统计词频，取前1000个词作为爬虫的查询关键词。
# 4.将结果写入文件中。
import re
import os
import jieba
from collections import Counter


class Config(object):
    def __init__(self):
        self.file_list_path = "data/"  # 用于分词的语料的存储位置
        self.keep_word_num = 1000  # 取前1000个词作为查询关键词
        self.output_file_path = "data/output.txt"  # 高频词的输出位置
        self.stop_words_path = "data/hagongda.txt"  # 使用哈工大开源的停用词表
        self.drop_NotChinese = True  # 默认去除非中文


def read_stop_words(stop_words_path):
    with open(stop_words_path, 'rt', encoding="utf-8") as f_stop:
        stop_words = f_stop.read().split("\n")
        return stop_words


def read_text_file(config):
    file_names = os.listdir(config.file_list_path)  # 获取到文件的名字
    file_list = [os.path.join(config.file_list_path, file) for file in file_names]  # 获取到文件的完整路径
    res = {}  # 用于存储输出结果，键为词汇，值为出现的次数
    stop_words = read_stop_words(config.stop_words_path)
    for file in file_list:
        with open(file, "rt", encoding="utf-8") as f:
            for line in f:
                words = jieba.cut(line)
                for word in words:
                    word = word.strip()  # 去除词汇左右的空白
                    if config.drop_NotChinese:
                        word=re.sub('[^\u4e00-\u9fff]+', '',word) # 过滤掉非中文
                    if word and word not in stop_words:
                        if word not in res:
                            res[word] = 1
                        else:
                            res[word] += 1
    return res


def write_MostCommonWords(config, word_count_dict):
    counter = Counter(word_count_dict)
    select_res = counter.most_common(config.keep_word_num)
    with open(conf.output_file_path, "wt", encoding="utf-8") as f_out:
        for item in select_res:
            f_out.write(str(item[0]) + "\t" + str(item[1]) + "\n")


def main(conf):
    word_count_dict = read_text_file(conf)
    write_MostCommonWords(conf, word_count_dict)


if __name__ == '__main__':
    conf = Config()  # 可以根据自己的项目需求修改配置
    main(conf)
