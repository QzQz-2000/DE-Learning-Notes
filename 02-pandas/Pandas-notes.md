[TOC]

# Pandas

## What is Pandas?

Pandas 是一个开源的数据分析和数据处理库，它是基于 Python 编程语言的。

Pandas 提供了易于使用的数据结构和数据分析工具，特别适用于处理结构化数据，如表格型数据（类似于Excel表格）。

Pandas 是数据科学和分析领域中常用的工具之一，它使得用户能够轻松地从各种数据源中导入数据，并对数据进行高效的操作和分析。

## 数据结构

Pandas 主要引入了两种新的数据结构：**DataFrame** 和 **Series**。

- Series: 类似于一维数组或者列表，是由一组数据以及与之相关的数据标签（索引）组成的。Series可以看成是DataFrame中的一列，也可以是单独存在的一维数据结构。

  - 索引：每个Series都有一个索引，可以是整数、字符串、日期等类型。如果不指定索引，pandas将默认创建一个从0开始的整数索引。
  - 数据类型：Series可以容纳不同数据类型的元素，包括整数、浮点数、字符串、python对象等。
  - 大小不变：创建之后Series的大小不变，但是可以通过某些操作（append或delete）来改变。
  - 操作：支持各种操作，如数学运算、统计分析、字符串处理等.
  - 缺失数据：可以包含缺失数据，使用NaN表示。

  ![1](./images/1.png)

  可以使用 pd.Series() 构造函数创建一个 Series 对象，传递一个数据数组（可以是列表、NumPy 数组等）和一个可选的索引数组。

  ```python
  pandas.Series(data=None, index=None, dtype=None, name=None, copy=False, fastpath=False)
  ```

  - data：数据部分，可以是列表、数组、字典等
  - index：索引部分，对数据进行标记，如果不提供则创建一个默认的整数索引
  - dtype：数据类型，如果不提供，则自动推断
  - name：名称，标识Series对象
  - copy：是否复制数据，默认为false
  - fastpath：是否启用快速路径，默认为false。启动快速路径在某些情况下可以提高性能

  提供索引：

  ```python
  import pandas as pd
  
  a = ["Google", "Runoob", "Wiki"]
  
  myvar = pd.Series(a, index = ["x", "y", "z"])
  
  print(myvar)
  ```

  我们也可以使用 key/value 对象，类似字典来创建 Series：

  ```python
  import pandas as pd
  
  sites = {1: "Google", 2: "Runoob", 3: "Wiki"}
  
  myvar = pd.Series(sites)
  
  print(myvar)
  ```

  这里的字典key变为了索引值。如果我们只需要字典中的一部分数据，只需要指定需要数据的索引即可，如下实例：

  ```python
  import pandas as pd
  
  sites = {1: "Google", 2: "Runoob", 3: "Wiki"}
  
  myvar = pd.Series(sites, index = [1, 2])
  
  print(myvar)
  ```

  使用列表、字典或者数组创建一个默认索引的Series：

  ```python
  # 使用列表创建 Series
  s = pd.Series([1, 2, 3, 4])
  
  # 使用 NumPy 数组创建 Series
  s = pd.Series(np.array([1, 2, 3, 4]))
  
  # 使用字典创建 Series
  s = pd.Series({'a': 1, 'b': 2, 'c': 3, 'd': 4})
  ```

  基本运算：

  ```python
  # 算术运算
  result = series * 2  # 所有元素乘以2
  
  # 过滤
  filtered_series = series[series > 2]  # 选择大于2的元素
  
  # 数学函数
  import numpy as np
  result = np.sqrt(series)  # 对每个元素取平方根
  ```

  属性和方法：

  ```python
  # 获取索引
  index = s.index
  
  # 获取值数组
  values = s.values
  
  # 获取描述统计信息
  stats = s.describe()
  
  # 获取最大值和最小值的索引
  max_index = s.idxmax()
  min_index = s.idxmin()
  
  # 其他属性和方法
  print(s.dtype)   # 数据类型
  print(s.shape)   # 形状
  print(s.size)    # 元素个数
  print(s.head())  # 前几个元素，默认是前 5 个
  print(s.tail())  # 后几个元素，默认是后 5 个
  print(s.sum())   # 求和
  print(s.mean())  # 平均值
  print(s.std())   # 标准差
  print(s.min())   # 最小值
  print(s.max())   # 最大值
  ```

  转换数据类型：

  ```python
  s = s.astype('float64')  # 将 Series 中的所有元素转换为 float64 类型
  ```

  

- DataFrame：类似于一个二维表格，是Pandas中最重要的数据结构。可以看作是多个Series按照列排列构成的表格，既有行索引也有列索引，因此可以方便地进行列选择、过滤、合并等操作。

  ![2](./images/2.svg)

DataFrame 可视为由多个 Series 组成的数据结构：

![img](https://www.runoob.com/wp-content/uploads/2021/04/pandas-DataStructure.png)



Pandas提供了丰富的功能：

- 数据清洗：处理缺数据、重复数据等
- 数据转换：改变数据的形状、结构或者格式
- 数据分析： 进行统计分析、聚合、分组等
- 数据可视化：通过整合Matplotlib和Seaborn等库，进行数据可视化



## 实践（Leetcode数据库题目）

### [175. 组合两个表](https://leetcode.cn/problems/combine-two-tables/)

分析：两个表进行join，sql很好写，注意python的语法

```python
DataFrame.merge(right, how='inner', on=None, left_on=None, right_on=None, left_index=False, right_index=False, sort=False, suffixes=('_x', '_y'), copy=None, indicator=False, validate=None)
```

```python
import pandas as pd

def combine_two_tables(person: pd.DataFrame, address: pd.DataFrame) -> pd.DataFrame:
    
    result = pd.merge(person, address, on='personId', how='left')
    result = result[['firstName', 'lastName', 'city', 'state']]

    return result
```

### [181. 超过经理收入的员工](https://leetcode.cn/problems/employees-earning-more-than-their-managers/)

分析：用到了merge和filter，以及返回结果的rename

```python
import pandas as pd

def find_employees(employee: pd.DataFrame) -> pd.DataFrame:
    result = employee.merge(employee, left_on='managerId', right_on='id', how='left', suffixes=('_employee', '_manager'))
    
    # 添加筛选条件
    result = result[result['salary_employee'] > result['salary_manager']]
    
    result = result[['name_employee']].rename(columns={'name_employee': 'Employee'})

    return result
```

此时的代码还存在问题，就是明明不清晰，可以如下改正：

```python
import pandas as pd

def find_employees(employee: pd.DataFrame) -> pd.DataFrame:
    # 合并员工和经理的数据，使用左连接
    merged_df = employee.merge(employee, left_on='managerId', right_on='id', how='left', suffixes=('_employee', '_manager'))
    
    # 根据工资比较筛选出工资高于经理的员工
    filtered_df = merged_df[merged_df['salary_employee'] > merged_df['salary_manager']]
    
    # 选择所需的列，并重命名
    result = filtered_df[['name_employee']].rename(columns={'name_employee': 'Employee'})
    
    return result
```

### [182. 查找重复的电子邮箱](https://leetcode.cn/problems/duplicate-emails/)

分析：寻找重复项，使用duplicated函数

```python
DataFrame.duplicated(subset=None, keep='first')
```

参数：

- subset: 列标签或标签序列，可选

  仅考虑某些列来识别重复项，默认使用所有列。

- keep: {'first', 'last', False}，默认'first'

  确定要标记哪些重复项（如果有）。`first`：将重复项标记为`True`除第一次出现之外（第一次为false，剩下的都为true）。`last`：将重复项标记为`True`除最后一次出现之外（最后一个为false，前边出现的都为true）。false ：将所有重复项标记为`True`。

  - 注意这里是'first', 'last'以及False，前两种选择有引号，最后一种没有！

```python
import pandas as pd

def duplicate_emails(person: pd.DataFrame) -> pd.DataFrame:
    
    duplicate_emails = person[person.duplicated(['email'], keep=False)]['email'].unique()

    # 这行代码的作用是创建一个新的 Pandas DataFrame，其中包含一个名为 'Email' 的列，
    # 这一列的数据来自于 duplicate_emails DataFrame 中的 'email' 列。
    result = pd.DataFrame({'Email': duplicate_emails})

    return result
```

