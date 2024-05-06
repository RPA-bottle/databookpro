# DataBookPro
这是利用闲暇时间，基于影刀`DataBook`模块进行二次开发和封装，支持更加python风格的数据读写操作，类似于pandas。


# 基础使用
复制`databookpro.py`文件到当前流程文件夹下，通过相对路径导入`databookpro`即可使用。或者在影刀流程管理器内新建名为`databookpro.py`的python模块，将`databookpro.py`的内容复制到该文件即可使用。

下面是简单的例子。
```python
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

    # dbp会自动判断用户提供的键是列名称（由A-Z组成的字符串）还是列描述，
    # 如果是全新的列描述，会自动添加到新的一列。
    # 写入第三列数据并设置列描述为'Col3'
    dbp['Col3'] = [11, 12, 13, 14, 15]
    # 写入第四、五列数据
    dbp[['Col4', 'E']] = [[1, 2]]*5

    # 默认情况下，dbp会自动检测字面量的数据类型并进行相应的类型转换。
    # 获取A1单元格的数据。
    data = dbp.loc[1, 'A']
    print('data:', data, ', type:', type(data).__name__)
    data = dbp.loc[1, 'Col1']
    print('data:', data, ', type:', type(data).__name__)
    # 关闭数据类型自动转换功能
    dbp.auto_parse = False
    data = dbp.loc[1, 'A']
    print('data:', data, ', type:', type(data).__name__)
    # 开启数据类型自动自动转换功能
    dbp.auto_parse = True

    # dbp支持切片操作，无论是列切片还是行切片
    # 获取奇数行数据
    data = dbp.loc[::2]
    print(data)
    # 获取偶数列数据
    data = dbp.loc[:, 'B'::2]
    print(data)
    # 获取最后两行数据
    data = dbp.loc[-2:]
    print(data)

    # 默认情况下，dbp会返回列表类型的数据，但是，可以手动设置返回
    # `pandas.DataFrame`、`pandas.Series`类型的数据
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
```

# 注意
由于通过`databook.get_column_desc_by_name`获取列描述很耗时（每次~0.01秒），所以不要利用该模块来处理大数据。在使用dbp时，如果在影刀软件内打开数据表格页面，速度会很慢，因为影刀会动态地把数据渲染到数据表格内，非常耗时。

另外，`databookpro`与`pandas`的读写数据逻辑并不是完全一致的，显著的差异如下：
- 行号
  行号只能是整数，而且从1开始计数。
- 列名
  dbp会自动识别列名和列描述，列名只能是A-Z组成的字符串，例如：“A”和“AB”。pandas的列名是任意的，而且没有列描述。
- 布尔类型、函数类型的索引
  dbp目前暂不支持布尔类型、函数类型的索引（以后有空再考虑要不要支持），而pandas支持。
- 数据类型
  默认情况下，dbp会自动转换数据类型，而pandas不会。而且默认情况下，dbp返回的数据不是pandas的DataFrame、Series类型，而是字面量或者列表。可以通过`dbp.output_format`来修改放回的数据类型。




