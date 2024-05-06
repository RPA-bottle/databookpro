import unittest
from xbot.app import databook as db
from xbot import print

# 为dbp设置临时环境变量
import sys
module_path = __file__[:__file__.index('xbot_robot')]
sys.path.append(module_path)
from xbot_robot.databookpro import dbp

''' 
测试删除数据。
删除数据有两种方式，一种是使用del关键字：
>>> del dbp['A']
另一种是使用dbp.drop函数
>>> dbp.drop(1)
>>> dbp.drop('A', axis=1)
>>> dbp.drop(index=[1, 2])
>>> dbp.drop(columns=['A', 'B'])
'''

class Delitem(unittest.TestCase):
    '''测试删除数据。'''

    def setUp(self) -> None:
        dbp.auto_parse = False
        db.set_range(
            1, 'A', 
            [[1, 2, 3, 4], ['a', 'b', 'c', 'd'], [5, 6, 7, 8]]    
        )


    def test__del(self):
        del dbp['A']
        self.assertListEqual(db.get_range(1, 'A', 3, 'D'), 
                             [['', '2', '3', '4'], ['', 'b', 'c', 'd'], ['', '6', '7', '8']])
        del dbp['B'], dbp['C']
        self.assertListEqual(db.get_range(1, 'A', 3, 'D'), 
                             [['', '', '', '4'], ['', '', '', 'd'], ['', '', '', '8']])
        with self.assertRaises(KeyError):
            del dbp[['B', 'D']]


    def test__drop_by_labels(self):
        dbp.drop(1)
        self.assertListEqual(db.get_range(1, 'A', 3, 'D'), 
                        [['', '', '', ''], ['a', 'b', 'c', 'd'], ['5', '6', '7', '8']])
        dbp.drop('A', axis=1)
        self.assertListEqual(db.get_range(1, 'A', 3, 'D'), 
                        [['', '', '', ''], ['', 'b', 'c', 'd'], ['', '6', '7', '8']])
        dbp.drop(['B', 'C'], axis=1)
        self.assertListEqual(db.get_range(1, 'A', 3, 'D'), 
                        [['', '', '', ''], ['', '', '', 'd'], ['', '', '', '8']])
        

    def test__drop_by_index(self):
        dbp.drop(index=1)
        self.assertListEqual(db.get_range(1, 'A', 3, 'D'), 
                        [['', '', '', ''], ['a', 'b', 'c', 'd'], ['5', '6', '7', '8']])
        dbp.drop(index=[2, 3])
        self.assertListEqual(db.get_range(1, 'A', 3, 'D'), 
                [['', '', '', '']]*3)
        
    
    def test__drop_by_columns(self):
        dbp.drop(columns=['A'])
        self.assertListEqual(db.get_range(1, 'A', 3, 'D'), 
                        [['', '2', '3', '4'], ['', 'b', 'c', 'd'], ['', '6', '7', '8']])
        dbp.drop(columns=['B', 'C'])
        self.assertListEqual(db.get_range(1, 'A', 3, 'D'), 
                [['', '', '', '4'], ['', '', '', 'd'], ['', '', '', '8']])
        


    def tearDown(self) -> None:
        dbp.clear()


