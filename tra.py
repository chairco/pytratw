#-*- coding:utf-8 -*-
import requests

import pandas as pd
import numpy as np

from lxml import etree


def get_tra_data():
    url = 'https://www.railway.gov.tw/tw/CP.aspx?sn=3611'
    r = requests.get(url)
    html = etree.HTML(r.text)
    parser = '//*[@id="Table7"]/tbody/tr'
    root = html.xpath(parser)
    cols = []

    for i in range(1, len(root)):  # total 28 elements
        rows = []
        if i == 1:
            parser_sub = '{}[{}]/th'.format(parser, i)
        else:
            parser_sub = '{}[{}]/td'.format(parser, i)
        sub = html.xpath(parser_sub)

        for j in range(1, len(sub) + 1):  # each element has 8 fields
            row = html.xpath('{}[{}]'.format(parser_sub, j))[0].text
            if type(row) is str:
                row = row.strip()  # 去除字符串兩邊的空格
                if row == '':
                    try:  # 南樹林多了 tag <p></p>
                        rowp = html.xpath(
                            '{}[{}]/p'.format(parser_sub, j))[0].text
                        rowp = rowp.strip()
                        row = rowp
                    except Exception as e:
                        pass
                if row == '自基隆起':
                    row = '0'
                rows.append(row)
            # if row is <class 'NoneType'> type(row) == None
            # 竟然不成立？似乎是不考慮繼承關係造成
            elif isinstance(row, type(None)):
                row = html.xpath('{}[{}]/span'.format(parser_sub, j))[0].text
                row = row.strip()
                rows.append(row)

        cols.append(rows)

    return cols


def convert(datas=None):
    if datas is None:
        datas = {}

    res = dict()
    for i in range(1, len(datas)):  # remove header
        # if j is odds, create pair key and value
        # key is j-1, value is j
        for j in range(len(datas[i])):
            if j % 2 != 0 and datas[i][j - 1] != '':
                res.setdefault(datas[i][j - 1], float(datas[i][j]))

    res = sorted(res.items(), key=lambda x: x[1])
    res = dict(res)

    return res


def caculate(start, end, datas):
    if not isinstance(start, str):
        raise Exception(f"'start:{type(start)}', Invalid Input")
    if not isinstance(end, str):
        raise Exception(f"'start:{type(end)}', Invalid Input")

    way_long = abs(datas.get(start) - datas.get(end))

    return way_long


if __name__ == '__main__':
    datas = get_tra_data()
    c = convert(datas=datas)
    # c = convert()
    print(c, list(c.keys()))
