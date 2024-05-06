import unittest
from xbot.app import databook as db
from xbot import print

# 为dbp设置临时环境变量
import sys
module_path = __file__[:__file__.index('xbot_robot')]
sys.path.append(module_path)
from xbot_robot.databookpro import dbp

'''
测试通过dbp逐元素写入数据。所谓的逐元素写入，是指通过调用`db.set_cell`写入数据。
出现以下情况时，dbp会将将索引转换为列表：
- 当索引不是连续逐一递增时
- 行索引为整数，列索引为字符串
索引转换后，如果行索引和列索引都是列表，dbp就会逐元素吸入数据。

例如，以下的例子就会逐元素写入数据
>>> dbp.loc[1, 'A'] = 1
>>> dbp.loc[[1, 2, 3], 'A'] = [1, 2, 3]
>>> dbp.loc[[1, 2, 3], ['A']] = [1]

'''

class SetitemElemWise(unittest.TestCase):
    '''测试逐元素写入数据'''

    def setUp(self) -> None:
        db.clear()

    def test_set_01(self):
        dbp.loc[1, 'A'] = 1
        self.assertEqual(db.get_cell(1, 'A'), '1')

    def test_set_02(self):
        dbp.loc[1, 'A'] = [1, 2]
        self.assertEqual(db.get_cell(1, 'A'), '[1, 2]')
        dbp.loc[1, 'A'] = 1, 2
        self.assertEqual(db.get_cell(1, 'A'), '(1, 2)')

    def test_set_03(self):
        dbp.loc[[1, 2], 'A'] = 1
        self.assertEqual(db.get_column('A'), ['1', '1'])

    def test_set_04(self):
        dbp.loc[[1, 2], 'A'] = 1, 2
        self.assertEqual(db.get_column('A'), ['1', '2'])

    def test_set_05(self):
        dbp.loc[1, ['A', 'C']] = 1
        self.assertEqual(db.get_row(1), ['1', None, '1'])

    def test_set_06(self):
        dbp.loc[1, ['A', 'C']] = 1, 2
        self.assertEqual(db.get_row(1), ['1', None, '2'])
    
    def test_set_07(self):
        dbp.loc[[1, 2], ['A', 'C']] = 1, 2
        self.assertEqual(db.get_range(1, 'A', 2, 'C'), 
                         [['1', None, '2']]*2)

    def test_set_08(self):
        dbp.loc[[1, 2], ['A', 'C']] = [[1, 2], [3, 4]]
        self.assertEqual(db.get_range(1, 'A', 2, 'C'), 
                         [['1', None, '2'], ['3', None, '4']])
    

# del SetitemElemWise




