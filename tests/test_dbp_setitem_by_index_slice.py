import unittest
from xbot.app import databook as db
from xbot import print

# 为dbp设置临时环境变量
import sys
module_path = __file__[:__file__.index('xbot_robot')]
sys.path.append(module_path)
from xbot_robot.databookpro import dbp

# 测试行索引切片写入数据。例如：
# >>> dbp.loc[:3, 'A'] = 1
# 单值会根据具体行索引（idx）和列索引(names)，自动推导并转换为二维列表，然后
# 调用`db.set_range`来写入数据。


class SetitemByIndexSliceToEmptyDataBook(unittest.TestCase):
    '''在空databook的情况下，测试通过索引切片设置数据。'''
    def setUp(self):
        dbp.clear()

    def test_set_00(self):
        '''单值单列。'''
        dbp.loc[:, 'A'] = 1
        self.assertListEqual(db.get_column('A'), ['1'])

    def test_set_01(self):
        print('test_set_empty__multiple_values_single_col')
        dbp.loc[:, 'A'] = [1, 2, 3]
        self.assertListEqual(db.get_column('A'), ['1', '2', '3'])

    def test_set_02(self):
        dbp.loc[:, ['A', 'C']] = 1
        self.assertListEqual(db.get_row(1), ['1', None, '1'])

    def test_set_03(self):
        dbp.loc[:, ['A', 'C']] = [1, 2]
        self.assertListEqual(db.get_row(1), ['1', None, '2'])

    def test_set_04(self):
        dbp.loc[:, ['A', 'C']] = [[1, 2], [3, 4]]
        self.assertListEqual(db.get_range(1, 'A', 2, 'C'), [['1', None, '2'], ['3', None, '4']])

    def test_set_05(self):
        dbp.loc[2:4, 'A'] = 1
        self.assertListEqual(db.get_column('A'), [None, '1', '1', '1'])

    def test_set_06(self):
        dbp.loc[2:4, 'A'] = [1, 2, 3]
        self.assertListEqual(db.get_column('A'), [None, '1', '2', '3'])

    def test_set_07(self):
        dbp.loc[2:4, ['A', 'C']] = 1
        self.assertListEqual(db.get_range(1, 'A', 4, 'C'), [[None]*3]+[['1', None, '1']]*3)

    def test_set_08(self):
        dbp.loc[2:4, ['A', 'C']] = [1, 2]
        self.assertListEqual(db.get_range(1, 'A', 4, 'C'), [[None]*3]+[['1', None, '2']]*3)

    def test_set_09(self):
        dbp.loc[2:4, ['A', 'C']] = [[1, 2], [3, 4], [5, 6]]
        self.assertListEqual(db.get_range(1, 'A', 4, 'C'), 
                             [[None]*3]+[['1', None, '2'], ['3', None, '4'], ['5', None, '6']])

    def test_set_10(self):
        dbp.loc[dbp.shape[0]+1:] = [3, 3, 3]
        self.assertListEqual(db.get_range(1, 'A', 2, 'C'), 
                             [['3']*3, [None]*3])


    # def tearDown(self) -> None:
    #     dbp.clear()


class SetitemByIndexSlice(unittest.TestCase):
    '''
    在databook已有数据的情况下，测试通过索引切片设置数据。
    '''
    def setUp(self):
        db.clear()
        db.set_column('A', [1, 2, 3])

    def test_set_00(self):
        dbp.loc[:, 'A'] = 1
        self.assertListEqual(db.get_column('A'), ['1', '1', '1'])

    def test_set_01(self):
        dbp.loc[:, 'A'] = [3, 4, 5]
        self.assertListEqual(db.get_column('A'), ['3', '4', '5'])

    def test_set_02(self):
        dbp.loc[:, ['A', 'C']] = 1
        self.assertListEqual(db.get_range(1, 'A', 3, 'C'), [['1', None, '1']]*3)

    def test_set_03(self):
        dbp.loc[:, ['A', 'C']] = [1, 2]
        self.assertListEqual(db.get_range(1, 'A', 3, 'C'), [['1', None, '2']]*3)

    def test_set_04(self):
        dbp.loc[:, ['A', 'C']] = [[1, 2], [3, 4], [5, 6]]
        self.assertListEqual(
            db.get_range(1, 'A', 3, 'C'), 
            [['1', None, '2'], ['3', None, '4'], ['5', None, '6']]
        )
    
    def test_set_05(self):
        dbp.loc[2:4, 'A'] = 0
        self.assertListEqual(db.get_column('A'), ['1', '0', '0', '0'])

    def test_set_06(self):
        dbp.loc[2:4, 'A'] = [1, 2, 3]
        self.assertListEqual(db.get_column('A'), ['1', '1', '2', '3'])

    def test_set_07(self):
        dbp.loc[2:4, ['A', 'C']] = 1
        self.assertListEqual(db.get_range(1, 'A', 4, 'C'), 
                             [['1', None, None]]+[['1', None, '1']]*3)

    def test_set_08(self):
        dbp.loc[2:4, ['A', 'C']] = [1, 2]
        self.assertListEqual(db.get_range(1, 'A', 4, 'C'), 
                             [['1', None, None]]+[['1', None, '2']]*3)

    def test_set_09(self):
        dbp.loc[2:4, ['A', 'C']] = [[1, 2], [3, 4], [5, 6]]
        self.assertListEqual(db.get_range(1, 'A', 4, 'C'), 
                             [['1', None, None]]+[['1', None, '2'], ['3', None, '4'], ['5', None, '6']])
    
    def test_set_10(self):
        dbp.loc[dbp.shape[0]+1:] = [3, 3, 3]
        self.assertListEqual(db.get_range(1, 'A', 4, 'C'), 
                             [['1', None, None]]+[['2', None, None], ['3', None, None], ['3', '3', '3']])


# del SetitemByIndexSliceToEmptyDataBook, SetitemByIndexSlice