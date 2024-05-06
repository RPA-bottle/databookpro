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

class SetitemByDescriptions(unittest.TestCase):

    def setUp(self):
        dbp.clear()

    def test_set_0(self):
        dbp.loc[1, 'a'] = 3
        dbp.loc[1, 'b'] = [1, 2]
        self.assertListEqual(db.get_row(1), ['3', '[1, 2]'])

    
    def test_set_01(self):
        dbp.loc[1, ['a', 'b']] = 3
        self.assertListEqual(db.get_row(1), ['3', '3'])


    def test_set_02(self):
        dbp.loc[[1, 2], ['a', 'b']] = 3
        self.assertListEqual(db.get_range(1, 'A', 2, 'B'), [['3', '3']]*2)

    def test_set_03(self):
        db.set_column_desc_by_name('A', 'a')
        db.set_column_desc_by_name('B', 'b')
        db.set_column_desc_by_name('C', 'c')

        dbp.loc[[1, 2], :'b'] = 3
        self.assertListEqual(db.get_range(1, 'A', 2, 'B'), [['3', '3']]*2)

        dbp.loc[[1, 2], 'b':'c'] = 1
        self.assertListEqual(db.get_range(1, 'A', 2, 'C'), [['3', '1', '1']]*2)


# del SetitemByDescriptions



