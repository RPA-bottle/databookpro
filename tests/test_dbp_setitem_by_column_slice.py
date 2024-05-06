import unittest
from xbot.app import databook as db
from xbot import print

# 为dbp设置临时环境变量
import sys
module_path = __file__[:__file__.index('xbot_robot')]
sys.path.append(module_path)
from xbot_robot.databookpro import dbp


# 测试列索引切片写入数据。例如：
# >>> dbp.loc[1, 'A':'C'] = 1
# 单值会根据具体行索引（idx）和列索引(names)，自动推导并转换为二维列表，然后
# 调用`db.set_range`来写入数据。


class SetitemByColumnSliceToEmptyDataBook(unittest.TestCase):
    '''在空databook的情况下，测试通过列索引切片设置数据。'''
    def setUp(self):
        db.clear()

    def test_set_00(self):
        '''单值单行。'''
        dbp.loc[1, :'B'] = 1
        self.assertListEqual(db.get_row(1), ['1', '1'])

    def test_set_01(self):
        '''单值多行。'''
        dbp.loc[[1, 3], :'B'] = 1
        self.assertListEqual(db.get_range(1, 'A', 3, 'B'), 
                             [['1']*2,[None]*2, ['1']*2])

    def test_set_02(self):
        '''多值单行。'''
        dbp.loc[1, :'B'] = [1, 2]
        self.assertListEqual(db.get_row(1), ['1', '2'])

    def test_set_03(self):
        '''多值多行。'''
        dbp.loc[[1, 2], :'B'] = [1, 2]
        self.assertListEqual(db.get_range(1, 'A', 2, 'B'),[['1', '2']]*2)
        
    def test_set_04(self):
        '''多值多行多列。'''
        dbp.loc[[1, 2], :'B'] = [[1, 2], [3, 4]]
        self.assertListEqual(db.get_range(1, 'A', 2, 'B'),
                            [['1', '2'], ['3', '4']])
    
    def test_set_05(self):
        '''单值单行。'''
        dbp.loc[1, 'B':'C'] = 1
        self.assertListEqual(db.get_row(1), [None, '1', '1'])

    
class SetitemByColumnSlice(unittest.TestCase):
    '''在已经有数据的情况下，测试通过列索引切片设置数据。'''
    def setUp(self):
        db.clear()
        db.set_range(1, 'A', [[1, 2, 3], [4, 5, 6]])

    def test_set_00(self):
        '''单值单行。'''
        dbp.loc[1, :'B'] = 1
        self.assertListEqual(db.get_row(1), ['1', '1', '3'])

    def test_set_01(self):
        '''单值多行。'''
        dbp.loc[[1, 3], :'B'] = 1
        self.assertListEqual(db.get_range(1, 'A', 3, 'B'), 
                             [['1']*2,['4', '5'], ['1']*2])
        
    def test_set_02(self):
        '''多值单行。'''
        dbp.loc[1, :'B'] = [2, 1]
        self.assertListEqual(db.get_range(1, 'A', 2, 'C'), 
                             [['2', '1', '3'], ['4', '5', '6']])


    def test_set_03(self):
        '''多值多行。'''
        dbp.loc[[1, 2], :'B'] = [2, 1]
        self.assertListEqual(db.get_range(1, 'A', 2, 'C'), 
                             [['2', '1', '3'], ['2', '1', '6']])
        
    def test_set_04(self):
        '''多值多行多列。'''
        dbp.loc[[1, 2], :'B'] = [[2, 1], [4, 3]]
        self.assertListEqual(db.get_range(1, 'A', 2, 'C'),
                            [['2', '1', '3'], ['4', '3', '6']])
    
    def test_set_05(self):
        '''单值单行。'''
        dbp.loc[1, 'B':'C'] = 1
        self.assertListEqual(db.get_range(1, 'A', 2, 'C'), 
                             [['1', '1', '1'], ['4', '5', '6']])


# del SetitemByColumnSliceToEmptyDataBook, SetitemByColumnSlice