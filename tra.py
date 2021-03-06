#-*- coding:utf-8 -*-
import requests
import pandas as pd

from datetime import datetime
from requests.auth import HTTPBasicAuth
from lxml import etree

try:
    from .make_hmac import *  # create_hmac, base64_digest
except Exception as e:
    from make_hmac import *  # create_hmac, base64_digest


TRA_miles = 'https://www.railway.gov.tw/tw/CP.aspx?sn=3611'
PTX_url = 'http://ptx.transportdata.tw/MOTC'


def get_tra_data(url=TRA_miles):
    """crawler station miles from TRA web 
    types: url: str
    rtypes: cols: list in list
    """
    r = requests.get(url)
    html = etree.HTML(r.text)
    parser = '//*[@id="Table7"]/tbody/tr'
    root = html.xpath(parser)
    cols = []

    for i in range(1, len(root)):  # total 28 elements
        rows = []
        if i == 1:
            parser_sub = f'{parser}[{i}]/th'
        else:
            parser_sub = f'{parser}[{i}]/td'
        sub = html.xpath(parser_sub)
        for j in range(1, len(sub) + 1):  # each element has 8 fields
            row = html.xpath('{}[{}]'.format(parser_sub, j))[0].text
            if type(row) is str:
                row = row.strip()  # remove str both side empty or \r\n
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
            elif isinstance(row, type(None)):  # 嘉北多了 tag <span></span>
                row = html.xpath('{}[{}]/span'.format(parser_sub, j))[0].text
                row = row.strip()
                rows.append(row)

        cols.append(rows)

    return cols


def convert(datas=None):
    """conver raw data from TRA web to dict
    types: datas: list in list
    rtypes: res: dict
    """
    if datas is None:
        datas = []

    res = dict()
    for i in range(1, len(datas)):  # remove header
        # if j is odds, create pair key and value
        # key is j-1, value is j
        for j in range(len(datas[i])):
            if j % 2 != 0 and datas[i][j - 1] != '':
                res.setdefault(datas[i][j - 1], float(datas[i][j]))

    # sort by station's kill
    res = sorted(res.items(), key=lambda x: x[1])
    res = dict(res)

    return res


def caculate(start, end, datas):
    """caculate miles with different stations
    types: start: string
    types: end: string
    types: datas: dict
    rtypes: way_long: float
    """
    if not isinstance(start, str):
        raise Exception(f"'start:{type(start)}', Invalid Input")
    if not isinstance(end, str):
        raise Exception(f"'start:{type(end)}', Invalid Input")

    # price should be abs
    way_long = abs(datas.get(start) - datas.get(end))

    return way_long


def get_tra_price(OriginStation, DestinationStation):
    """caculate different stations prices by api
    types: OriginStation: str
    types: DestinationStation: str
    rtypes: r: json
    """
    OriginStationID = stationid_dict.get(OriginStation)[0]
    DestinationStationID = stationid_dict.get(DestinationStation)[0]

    # Here get HMAC object for authorization
    auth = create_hmac(secretkey=AppKey, message=message)
    signature = base64_digest(auth=auth)
    authorization = f'hmac username="{AppID}", algorithm="hmac-sha1", headers="x-date", signature="{signature}"'
    
    # use requests module to communication with PTX's api
    headers = {
        'Authorization': authorization,
        'x-date': x_date
    }
    resource = f'{PTX_url}/v2/Rail/TRA/ODFare/{OriginStationID}/to/{DestinationStationID}?$top=30&$format=JSON'
    r = requests.get(resource, headers=headers)
    return r


if __name__ == '__main__':
    #datas = get_tra_data()
    #c = convert(datas=datas)
    # c = convert()
    #print(c, list(c.keys()))
    #p = get_tra_price(OriginStation='基隆', DestinationStation='新左營')
    #print(p.status_code)

