#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json
import re


def give_tag(content):
    pattern_reason = re.compile(u'售房原因|换房')
    pattern_sincere = re.compile(u'诚心|诚意|着急')
    pattern_key = re.compile(u'钥匙|有钥匙')
    pattern_price = re.compile(u'价格|签约|商量|成交|低价|最低|付款|协商|变现')
    pattern_anytime = re.compile(u'随时|提前|方便|联系|提前联系|配合|预约|打电话')
    tag_list = []
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


if __name__ == '__main__':
    record = "我的钥匙呢，随时"
    text = give_tag(record)
    print(text)