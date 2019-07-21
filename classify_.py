# -*- coding:utf-8 -*-
"""
文本预处理、分词
:Author:  WangYong
:Create:  2019/7/18 20:25
Copyright (c) 2019, Beike Group All Rights Reserved.
"""
import json
import pandas as pd
import re
import jieba
import pickle
from collections import Counter
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report,accuracy_score
from sklearn.feature_extraction.text import TfidfTransformer,CountVectorizer


# 数据加载和预处理
def preprocess(path):
    dic = {"housedelCode": [], "followUpContent": []}
    with open(path, "r", encoding="utf-8") as f:
        for line in f.readlines():
            line_dic = json.loads(line)
            for x in line_dic["followUps"]:
                dic["housedelCode"].append(line_dic["housedelCode"])
                content = x["followUpContent"]
                # 中文过滤
                content = re.sub(u"[^\u4e00-\u9fa5]", "", content)
                content_ = " ".join(jieba.cut(content))
                dic["followUpContent"].append(content_)
        df = pd.DataFrame(dic)
        with open("./df.data", "wb") as f:
            pickle.dump(df, f)
        return df


# 统计词频
def tj():
    with open("./df.data", "rb") as f:
        data = pickle.load(f)
    l = []
    for i in data["followUpContent"].values:
        l.extend(i.split(" "))
    res = Counter(l).most_common()
    print(res)


def pre_process_txt(path):
    dic = {"feat": [], "label": []}
    li = []
    with open(path, "r+", encoding="utf-8") as f:
        for line in f.readlines():
            tmp = line.split(";")
            content = "".join(tmp[:-1])
            content = re.sub(u"[^\u4e00-\u9fa5]", "", content)
            content_ = " ".join(jieba.cut(content))
            if len(tmp) <= 2:
                try:
                    dic["label"].append(re.sub("\n", "", tmp[1].strip()))
                    dic["feat"].append(content_)
                except Exception as e:
                    li.append(content_)
            else:
                dic["label"].append(re.sub("\n", "", tmp[-1]))
                dic["feat"].append(content_)
    train_df = pd.DataFrame(dic)
    return train_df, li


def tag_classify(train_set):
    # 向量化选择tfidf向量化
    c_vector = CountVectorizer()
    X, Y = train_set["feat"].values, train_set["label"].values
    x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=0)
    tfidf = TfidfTransformer()
    tfidf_model = tfidf.fit_transform(c_vector.fit_transform(x_train))
    with open("./classify/conf/tfidf.model", "wb") as f1:
        pickle.dump(tfidf, f1)
    with open("./classify/conf/c_vector.model", "wb") as f2:
        pickle.dump(c_vector, f2)
    x_train = tfidf_model.toarray()
    x_test = tfidf.transform(c_vector.transform(x_test)).toarray()
    # 贝叶斯模型
    clf_bayes = MultinomialNB(alpha=0.01)
    clf_bayes.fit(x_train, y_train)
    with open("./classify/conf/clf_bayes.model", "wb") as ff:
        pickle.dump(clf_bayes, ff)
    print(classification_report(y_test, clf_bayes.predict(x_test)))


if __name__ == "__main__":
    tr, te = pre_process_txt("./dd2.txt")
    tag_classify(tr)