#-*- coding: utf-8 -*-
import unittest

try:
    from . import tra
except Exception as e:
    import tra


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
        self.assertEqual(self.datas[1], ['基隆', '0', '新豐', '95.8', '員林', '225.6', '永康', '346.8'])

    def test_caculate(self):
        self.assertEqual(self.ntos, 391.3)
        self.assertEqual(self.ston, 391.3)



if __name__ == '__main__':
    unittest.main()