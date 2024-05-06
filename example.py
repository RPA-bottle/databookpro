from xbot import print
from .databookpro import dbp

def main(args):
    # 清空数据列表
    dbp.clear()
    # 设置列描述
    dbp.descs = ['Col1', 'Col2']
    # 写入第一行数据
    dbp.loc[1] = [1, 2]
    # 写入第二、三行数据
    dbp.loc[[2, 3]] = [[3, 4], [5, 6]]
    # 写入第四、五行数据
    dbp.loc[4:] = [[7, 8], [9, 10]]
    # 写入第三列数据
    dbp['Col3'] = [11, 12, 13, 14, 15]
    # 写入第四、五列数据
    dbp[['Col4', 'E']] = [[1, 2]]*5

    # 获取A1单元格的数据。默认情况下，dbp会自动检测字面量的数据类型并进行相应的类型转换。
    data = dbp.loc[1, 'A']
    print('data:', data, ', type:', type(data).__name__)
    data = dbp.loc[1, 'Col1']
    print('data:', data, ', type:', type(data).__name__)

    # 关闭数据类型自动自动转换功能
    dbp.auto_parse = False
    data = dbp.loc[1, 'A']
    print('data:', data, ', type:', type(data).__name__)
    # 开启数据类型自动自动转换功能
    dbp.auto_parse = True


    # 获取奇数行数据
    data = dbp.loc[::2]
    print(data)
    # 获取偶数列数据
    data = dbp.loc[:, 'B'::2]
    print(data)
    # 获取最后两行数据
    data = dbp.loc[-2:]
    print(data)

    # 默认情况下，dbp会返回列表类型的数据，但是，可以设置返回`pandas.DataFrame`、`pandas.Series`的数据类型
    dbp.output_format = 'pandas'
    # 获取第一行数据，数据类型将是`pandas.Series`类型
    data = dbp.loc[1]
    print(data)
    # 获取第一列数据，数据类型将是`pandas.Series`类型
    data = dbp['A']
    print(data)
    # 获取前两行、前两列数据，数据类型将是`pandas.DataFrame`类型
    data = dbp.loc[:2, :'B']
    print(data)