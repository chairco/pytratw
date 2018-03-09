#-*- coding: utf-8 -*-
import unittest

try:
    from . import tra
except Exception as e:
    import tra


west_stations = [
    '基隆', '三坑', '八堵', '七堵', '百福', '五堵', '汐止', '汐科',
    '南港', '松山', '臺北', '萬華', '板橋', '浮洲', '樹林', '南樹林',
    '山佳', '鶯歌', '桃園', '內壢', '中壢', '埔心', '楊梅', '富岡',
    '新富', '北湖', '新豐', '竹北', '北新竹', '新竹', '三姓橋', '香山',
    '崎頂', '竹南', '造橋', '豐富', '苗栗', '南勢', '銅鑼', '三義',
    '泰安', '后里', '豐原', '潭子', '太原', '臺中', '大慶', '烏日',
    '新烏日', '成功', '彰化', '花壇', '員林', '永靖', '社頭', '田中',
    '二水', '林內', '石榴', '斗六', '斗南', '石龜', '大林', '民雄', '嘉北', '嘉義',
    '水上', '南靖', '後壁', '新營', '柳營', '林鳳營', '隆田', '拔林', '善化', '南科',
    '新市', '永康', '大橋', '臺南', '保安', '仁德', '中洲', '大湖', '路竹', '岡山',
    '橋頭', '楠梓', '新左營', '左營', '高雄', '鳳山', '後庄', '九曲堂', '六塊厝', '屏東'
]


class TestTRA(unittest.TestCase):

    def log(self, msg):
        objid = hex(id(self))
        print(f"<<{objid}>>: {msg} -- {self._testMethodName}")

    def setUp(self):
        self.datas = tra.get_tra_data()
        self.convert = tra.convert(datas=self.datas)
        self.ntos = tra.caculate(start='基隆', end='新左營', datas=self.convert)
        self.ston = tra.caculate(start='新左營', end='基隆', datas=self.convert)

    def tearDown(self):
        self.log('tearDownnvoked.')

    def test_getdata(self):
        self.assertEqual(len(self.datas), 27)
        self.assertEqual(
            self.datas[1], ['基隆', '0', '新豐', '95.8', '員林', '225.6', '永康', '346.8'])

    def test_caculate(self):
        self.assertEqual(self.ntos, 391.3)
        self.assertEqual(self.ston, 391.3)

    def test_station_count(self):
        # West's station count
        self.assertEqual(len(self.convert.keys()), 96)
        self.assertEqual(list(self.convert.keys()), west_stations)
        

if __name__ == '__main__':
    unittest.main()
