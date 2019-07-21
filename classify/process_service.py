# -*- coding:utf-8 -*-
"""
请求的逻辑处理部分
:Author:  WangYong
:Create:  2019/7/4 17:55
Copyright (c) 2019, Beike Group All Rights Reserved.
"""
import json
import re
import jieba
import pickle
"""
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import pandas as pd
from collections import Counter
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report,accuracy_score
from sklearn.feature_extraction.text import TfidfTransformer,CountVectorizer
"""


class Process:
    def __init__(self, request_body):
        self.request_body_j = json.loads(request_body)
        self._data_load()

    def _data_load(self):
        # 项目相关内容:项目名称、当前分支
        self.content = self.request_body_j["content"]

    def classify_tag(self):
        l = []
        for content in self.content:
            content = re.sub(u"[^\u4e00-\u9fa5]", "", content)
            content_ = " ".join(jieba.cut(content))
            l.append(content_)
        with open("./conf/tfidf.model", "rb") as f1:
            tfidf = pickle.load(f1)
        with open("./conf/c_vector.model", "rb") as f2:
            c_vector = pickle.load(f2)
        with open("./conf/clf_bayes.model", "rb") as f3:
            model_ = pickle.load(f3)
        x = tfidf.transform(c_vector.transform(l)).toarray()
        y = model_.predict(x)
        return list(y)

    def give_tag(self):
        tag_list = []
        for content in self.content:
            pattern_reason = re.compile(u'售房原因|换房')
            pattern_sincere = re.compile(u'诚心|诚意|着急')
            pattern_key = re.compile(u'钥匙|有钥匙')
            pattern_price = re.compile(u'价格|签约|商量|成交|低价|最低|付款|协商|变现')
            pattern_anytime = re.compile(u'随时|提前|方便|联系|提前联系|配合|预约|打电话')
            result_reason = pattern_reason.findall(content)
            result_sincere = pattern_sincere.findall(content)
            result_key = pattern_key.findall(content)
            result_price = pattern_price.findall(content)
            result_anytime = pattern_anytime.findall(content)
            if result_reason:
                tag_list.append('售房原因')
            if result_sincere:
                tag_list.append('诚心卖')
            if result_key:
                tag_list.append('钥匙')
            if result_price:
                tag_list.append('价格')
            if result_anytime:
                tag_list.append('时间')
        return tag_list

    def my_service(self):
        dic = {"class": self.classify_tag(), "tag": self.give_tag()}
        print(dic)
        return dic

