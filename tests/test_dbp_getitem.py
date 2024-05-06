import unittest
from xbot.app import databook as db
from xbot import print

# 为dbp设置临时环境变量
import sys
module_path = __file__[:__file__.index('xbot_robot')]
sys.path.append(module_path)
from xbot_robot.databookpro import dbp

# 测试获取数据。
# >>> data = dbp.loc[:3, :'B']


class GetitemWithoutParsed(unittest.TestCase):
    '''测试获取数据。'''
    def setUp(self) -> None:
        dbp.auto_parse = False
        db.set_range(
            1, 'A', 
            [[1, 2, 3, 4], ['a', 'b', 'c', 'd'], [5, 6, 7, 8]]    
        )
    
    def test_getitem(self):
        self.assertEqual(dbp.loc[1, 'A'], '1')
        self.assertEqual(dbp.loc[2, 'A'], 'a')
        self.assertListEqual(dbp.loc[:, 'A'], ['1',  'a', '5'])
        self.assertListEqual(dbp.loc[:, :], [['1', '2', '3', '4'], ['a', 'b', 'c', 'd'], ['5', '6', '7', '8']])
        self.assertListEqual(dbp.loc[:, 'B':], [['2', '3', '4'], ['b', 'c', 'd'], ['6', '7', '8']])
        self.assertListEqual(dbp.loc[:, :'B'], [['1', '2'], ['a', 'b'], ['5', '6']])
        self.assertListEqual(dbp.loc[1:2, 'B'], ['2', 'b'])
        self.assertListEqual(dbp.loc[1:3, 'B'], ['2', 'b', '6'])
        self.assertListEqual(dbp.loc[1:2, ['B', 'C']], [['2', '3'], ['b', 'c']])
        self.assertListEqual(dbp.loc[1:2, 'B':'C'], [['2', '3'], ['b', 'c']])
        self.assertListEqual(dbp.loc[2:3, 'B':'C'], [['b', 'c'], ['6', '7']])
        self.assertListEqual(dbp.loc[1:2, :'D'], [['1', '2', '3', '4'], ['a', 'b', 'c', 'd']])
        self.assertListEqual(dbp.loc[1:2, :'D':2], [['1', '3'], ['a', 'c']])
        self.assertListEqual(dbp.loc[:3, :'D'], [['1', '2', '3', '4'], ['a', 'b', 'c', 'd'], ['5', '6', '7', '8']])
        self.assertListEqual(dbp.loc[:3:2, :'D':2], [['1', '3'], ['5', '7']])
        self.assertListEqual(dbp.loc[-2:, 'A'], ['a', '5'])
        self.assertListEqual(dbp.loc[-2:-1, 'C':], [['c', 'd'], ['7', '8']])
        self.assertListEqual(dbp.loc[-1:-10:-1, 'C':], [['7', '8'], ['c', 'd'], ['3', '4']])
        self.assertListEqual(dbp.loc[-1:-10:-1, 'D':'A':-2], [['8', '6'], ['d', 'b'], ['4', '2']])


class GetitemWithParsedNumber(unittest.TestCase):
    '''测试获取数据。'''
    def setUp(self) -> None:
        dbp.auto_parse = True
        db.set_range(
            1, 'A', 
            [[1, 2, 3, 4], ['a', 'b', 'c', 'd'], [5, 6, 7, 8]]    
        )


    def test_getitem(self):
        self.assertEqual(dbp.loc[1, 'A'], 1)
        self.assertEqual(dbp.loc[2, 'A'], 'a')
        self.assertListEqual(dbp.loc[:, 'A'], [1,  'a', 5])
        self.assertListEqual(dbp.loc[:, :], [[1, 2, 3, 4], ['a', 'b', 'c', 'd'], [5, 6, 7, 8]])
        self.assertListEqual(dbp.loc[:, 'B':], [[2, 3, 4], ['b', 'c', 'd'], [6, 7, 8]])
        self.assertListEqual(dbp.loc[:, :'B'], [[1, 2], ['a', 'b'], [5, 6]])
        self.assertListEqual(dbp.loc[1:2, 'B'], [2, 'b'])
        self.assertListEqual(dbp.loc[1:3, 'B'], [2, 'b', 6])
        self.assertListEqual(dbp.loc[1:2, ['B', 'C']], [[2, 3], ['b', 'c']])
        self.assertListEqual(dbp.loc[1:2, 'B':'C'], [[2, 3], ['b', 'c']])
        self.assertListEqual(dbp.loc[2:3, 'B':'C'], [['b', 'c'], [6, 7]])
        self.assertListEqual(dbp.loc[1:2, :'D'], [[1, 2, 3, 4], ['a', 'b', 'c', 'd']])
        self.assertListEqual(dbp.loc[1:2, :'D':2], [[1, 3], ['a', 'c']])
        self.assertListEqual(dbp.loc[:3, :'D'], [[1, 2, 3, 4], ['a', 'b', 'c', 'd'], [5, 6, 7, 8]])
        self.assertListEqual(dbp.loc[:3:2, :'D':2], [[1, 3], [5, 7]])
        self.assertListEqual(dbp.loc[-2:, 'A'], ['a', 5])
        self.assertListEqual(dbp.loc[-2:-1, 'C':], [['c', 'd'], [7, 8]])
        self.assertListEqual(dbp.loc[-1:-10:-1, 'C':], [[7, 8], ['c', 'd'], [3, 4]])
        self.assertListEqual(dbp.loc[-1:-10:-1, 'D':'A':-2], [[8, 6], ['d', 'b'], [4, 2]])


class GetitemParseNotNumberType(unittest.TestCase):
    '''测试通过dbp获取非数值类型的变量，例如字典、列表等。'''

    def setUp(self) -> None:
        dbp.auto_parse = True
        dbp.clear()


    def test_getitem(self):
        dbp.loc[1, 'A'] = [1, 2, 3]
        self.assertListEqual(dbp.loc[1, 'A'], [1, 2, 3])
        dbp.loc[1, 'B'] = {1, 2, 'a'}
        self.assertSetEqual(dbp.loc[1, 'B'], {1, 2, 'a'})
        dbp.loc[1, 'A'] = {1:'a', 2:'b', 'a':'c'}
        self.assertDictEqual(dbp.loc[1, 'A'], {1:'a', 2:'b', 'a':'c'})
        dbp.loc[1, 'B'] = 'ab'
        self.assertEqual(dbp.loc[1, 'B'], 'ab')
    

# del GetitemWithoutParsed, GetitemWithParsedNumber, GetitemParseNaN