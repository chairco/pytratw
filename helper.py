#-*- coding: utf-8 -*-
import requests

from lxml import etree
from typing import Dict, List, Tuple


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-TW,zh;q=0.9,zh-CN;q=0.8,en-US;q=0.7,en;q=0.6,ja;q=0.5,ru;q=0.4,mt;q=0.3,fr;q=0.2',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Content-Length': '83',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie': '_ga=GA1.3.1181475155.1578616708; JSESSIONID=Ew4x9T37qatGHvPDZH4xnS8vMOdzHKvV1_YPbIQfVLZkzI4WsfyJ!-584654896; _gid=GA1.3.451895859.1581386126',
    'Host': 'www.railway.gov.tw',
    'Origin': 'https://www.railway.gov.tw',
    'Referer': 'https://www.railway.gov.tw/tra-tip-web/tip/tip00C/tipC14/query',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
}


def get_csrf(client, url, p, headers) -> str:
    """
    headers: Dict: browser post requests's headers
    """
    r = client.get(url)

    html = etree.HTML(r.content.decode())
    csrf = html.xpath(p)[0].values()[2] if len(html.xpath(
        p)[0].values()) == 3 else None  # csrf token at input form

    return csrf


def get_senven_km(headers: Dict) -> Dict:
    """
    headers: Dict: browser post request's headers
    """
    url = 'https://www.railway.gov.tw/tra-tip-web/tip/tip00C/tipC14/query'
    p = '//*[@id="queryBlock"]/input'

    client = requests.session()
    csrf = get_csrf(client, url, p, headers)

    data = {
        '_csrf': csrf,
        'station': '4340-新左營'
    }

    res = client.post(url, headers=headers, data=data)

    stations_dict = {}
    for i in range(5, 8):
        p = f'//*[@id="content"]/div[{i}]/table/'
        group = f'{p}/tr[1]//text()'
        s = {}

        same = f'{p}/tr[1]/td[2]//text()'
        opposite = f'{p}/tr[2]/td[2]//text()'

        parser = etree.HTMLParser(encoding="utf-8")
        html = etree.HTML(res.text, parser=parser)

        #html = etree.HTML(res.content.decode())
        #station_lists = html.xpath(pp)
        # print(station_lists)

        group = list(filter(None, [s.rstrip() for s in html.xpath(group)]))
        # print(group[0])

        # del \r\n\t then del empty str
        station_lists_same = list(
            filter(None, [s.rstrip() for s in html.xpath(same)]))
        # print(f"順行: {station_lists_same}")
        s[f'順行'] = station_lists_same

        station_lists_opposite = list(filter(
            None, [s.rstrip() for s in html.xpath(opposite)]))  # del \r\n\t then del empty str
        # print(f"逆行: {station_lists_opposite} \n")
        s[f'逆行'] = station_lists_opposite

        stations_dict[group[0]] = s

    return stations_dict


def get_prices(start: str, end: str, headers: Dict) -> Dict:
    """
    headers: Dict: browser post requests's headers
    """
    print(start, end)
    url = 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip114/query'
    p = '//*[@id="queryBlock"]/input'

    client = requests.session()    
    csrf = get_csrf(client, url, p, headers)

    data = {
        '_csrf': csrf,
        'tip114QueryVOs[0].ticketDeadlineType': 'ELECTRONIC_TICKET',
        'tip114QueryVOs[0].startStation': start,
        'tip114QueryVOs[0].endStation': end,
        'tip114QueryVOs[0].trainType': '6',
        'tip114QueryVOs[0].ticketPriceType': '1',
        'tip114QueryVOs[0].ticketCount': '1'
    }

    return data


if __name__ == '__main__':
    from pprint import pprint
    
    pprint(get_senven_km(headers=headers))
    #print(get_prices(start='4340-新左營', end='3470-斗六', headers=headers))


