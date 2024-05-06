import unittest
from xbot.app import databook as db
from xbot import print

# 为dbp设置临时环境变量
import sys
module_path = __file__[:__file__.index('xbot_robot')]
sys.path.append(module_path)
from xbot_robot.databookpro import dbp

# 测试行索引切片和列索引切片写入数据。例如：
# >>> dbp.loc[:3, :'B'] = 1
# 单值会根据具体行索引（idx）和列索引(names)，自动推导并转换为二维列表，然后
# 调用`db.set_range`来写入数据。


class SetitemByBothSliceToEmptyDataBook(unittest.TestCase):
    '''在空databook的情况下，测试通过索引切片设置数据。'''
    def setUp(self):
        db.clear()

    def test_set_00(self):
        dbp.loc[:2, :'C'] = 2
        self.assertListEqual(db.get_range(1, 'A', 2, 'C'), [['2', '2', '2']]*2)
    
    def test_set_01(self):
        dbp.loc[:2, 'B':'C'] = 2
        self.assertListEqual(db.get_range(1, 'A', 2, 'C'), [[None, '2', '2']]*2)

    def test_set_02(self):
        dbp.loc[2:3, 'B':'C'] = 2
        self.assertListEqual(db.get_range(1, 'A', 3, 'C'), [[None]*3]+[[None, '2', '2']]*2)

    def test_set_03(self):
        dbp.loc[:2, 'B':'C'] = [1, 2]
        self.assertListEqual(db.get_range(1, 'A', 2, 'C'), [[None, '1', '2']]*2)

    def test_set_04(self):
        dbp.loc[:2, 'B':'C'] = [[1, 2], [3, 4]]
        self.assertListEqual(db.get_range(1, 'A', 2, 'C'), 
                             [[None, '1', '2'], [None, '3', '4']])
        
    def test_set_05(self):
        dbp.loc[2:3, 'B':'C'] = [[1, 2], [3, 4]]
        self.assertListEqual(db.get_range(1, 'A', 3, 'C'), 
                             [[None]*3, [None, '1', '2'], [None, '3', '4']])
        
    def test_set_06(self):
        dbp.loc[2:, 'B':'C'] = [[1, 2], [3, 4]]
        self.assertListEqual(db.get_range(1, 'A', 3, 'C'), 
                             [[None]*3, [None, '1', '2'], [None, '3', '4']])

    def test_set_07(self):
        dbp.loc[2:3, 'B':] = [[1, 2], [3, 4]]
        self.assertListEqual(db.get_range(1, 'A', 3, 'C'), 
                             [[None]*3, [None, '1', '2'], [None, '3', '4']])

# del SetitemByBothSliceToEmptyDataBook


