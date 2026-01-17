# Numpy使用教程

## 基本信息

### Numpy 介绍
NumPy（Numerical Python）是 Python 科学计算与数据分析的核心基础库，提供高效的同构多维数组（ndarray）作为核心数据结构，底层由 C 语言实现，相比原生 Python 列表大幅提升内存效率与数值计算速度，支持向量化操作、广播机制及丰富的数学/统计/线性代数函数（如矩阵运算、傅里叶变换、均值方差计算等），是 Pandas、Matplotlib、Scikit-learn 等主流数据科学工具的底层依赖，广泛用于数值模拟、数据预处理、机器学习等场景，常规通过 import numpy as np 导入使用。

## ndarray

### 1. ndarray特点
    1. 多维性：支持0维（标量），1维（向量），2维（矩阵）及更高维数组
    2. 同质性：所以元素类型必须一致
    3. 高效性：基于连续内存块存储，支持向量化运算


```python
import numpy as np

# 多维性
print("创建0维数组")
arr0 = np.array(5)   # 创建0维ndarray
print('arr0：',arr0)
print('arr0的维度：',arr0.ndim)    # number of dimensions

print("\n创建1维数组")
arr1 = np.array([1,2,3]) # 创建1维ndarray
print('arr1：',arr1)
print('arr1的维度：',arr1.ndim)

print("\n创建2维数组")
arr2 = np.array([[1,2,3],[4,5,6]])
print('arr2：',arr2)
print('arr2的维度：',arr2.ndim)
```

    创建0维数组
    arr0： 5
    arr0的维度： 0
    
    创建1维数组
    arr1： [1 2 3]
    arr1的维度： 1
    
    创建2维数组
    arr2： [[1 2 3]
     [4 5 6]]
    arr2的维度： 2



```python
# 同质性
# 不同的数据类型会被强制转换成相同的数据类型
arr = np.array([1,'hello'])
print(arr)

brr = np.array([1,2.5])
print(brr)
```

    ['1' 'hello']
    [1.  2.5]


### 2. ndarray的属性


|   属性名称   | 通俗解释         |     使用示例     |
|:--------:|:-------------|:------------:|
|  shape   | 数组的形状        |  arr.shape   |
|   ndim   | 维度数量         |   arr.ndim   |
|   size   | 总元素个数        |   arr.size   |
|  dtype   | 元素类型         |   arr.type   |
|    T     | 转置           |    arr.T     |
| itemsize | 单个元素占用的内存字节数 | arr.itemsize |
|  nbytes  | 数组总内存占用量     |  arr.nbytes  |
|  flags   | 内存存储方式（是否连续） |  arr.flags   |



```python
arr = np.array([[1,2,3],[4,5,6]])
print('数组的形状：',arr.shape)
print('维度的数量：',arr.ndim)
print('总元素个数：',arr.size)
print('元素类型：',arr.dtype)
```

    数组的形状： (2, 3)
    维度的数量： 2
    总元素个数： 6
    元素类型： int64


### 3. ndarray的创建

#### 基础方法


```python
# 基础的创建方法
list1 = [[1,2,3],[4,5,6]]

print('基础创建方法')
arr1 = np.array(list1)
print(arr1)

# 还可以用dtype强行指定类型
print('\n指定元素类型为浮点数：')
arr12 = np.array([[1,2,3],[4,5,6]],dtype=np.float64)
print(arr2)
```

    基础创建方法
    [[1 2 3]
     [4 5 6]]
    
    指定元素类型为浮点数：
    [[1 2 3]
     [4 5 6]]


#### 预定义形状
- array():基础创建方法
- zeros():用0填充
- ones():用1填充
- empty():未初始化（随机填充）
- full():指定数字填充


```python
# 全0
arr1 = np.zeros((2,3),dtype= int)    # 2行3列全0数组
print("2行3列全0数组：")
print(arr1)

# 1维全0
arr2 = np.zeros((2,),dtype= int)
print("\n1维全0数组：")
print(arr2)
```

    2行3列全0数组：
    [[0 0 0]
     [0 0 0]]
    
    1维全0数组：
    [0 0]



```python
# 全1
arr3 = np.ones((2,3),dtype= int)    # 2行3列全1数组
print("2行3列全1数组：")
print(arr3)
```

    2行3列全1数组：
    [[1 1 1]
     [1 1 1]]



```python
# 未初始化
arr4 = np.empty((2,3))
print("2行3列未初始化数组（随机填充数字）")
print(arr4)
```

    2行3列未初始化数组（随机填充数字）
    [[4.9e-324 9.9e-324 1.5e-323]
     [2.0e-323 2.5e-323 3.0e-323]]



```python
# 指定其他数字填充
arr5 = np.full((2,3),6)
print("2行3列用6填充")
print(arr5)
```

    2行3列用6填充
    [[6 6 6]
     [6 6 6]]


#### 基于数值范围创建


```python
# 生成等差数列
arr = np.arange(1,10,1) # start,end,step
print(arr)
```

    [1 2 3 4 5 6 7 8 9]



```python
# 等间隔序列
arr = np.linspace(1,10,5,dtype= int)
print(arr)
```

    [ 1  3  5  7 10]



```python
# 对数间隔序列
arr = np.logspace(0,4,3)
print(arr)

# base用于指定底数
arr1 = np.logspace(0,4,4, base = 2)
print(arr1)
```

    [1.e+00 1.e+02 1.e+04]
    [ 1.          2.5198421   6.34960421 16.        ]


#### 特殊矩阵的生成
- 零矩阵
- 单位矩阵:eye
- 对角矩阵:diag
- 对称矩阵


```python
# 单位矩阵
arr = np.eye(3) #默认行列相同
print(arr)

arr1 = np.eye(3,4) #三行四列
print("\n三行四列")
print(arr1)
```

    [[1. 0. 0.]
     [0. 1. 0.]
     [0. 0. 1.]]
    
    三行四列
    [[1. 0. 0. 0.]
     [0. 1. 0. 0.]
     [0. 0. 1. 0.]]



```python
# 对角矩阵
arr = np.diag([5,1,2,3])
print(arr)
```

    [[5 0 0 0]
     [0 1 0 0]
     [0 0 2 0]
     [0 0 0 3]]


#### 随机数组的生成


```python
# 生成0到1之间的随机浮点数
arr = np.random.rand(2,3)
print(arr)
```

    [[0.49407393 0.78840052 0.00279988]
     [0.81675041 0.65563969 0.44993513]]



```python
# 生成指定范围区间内的随机浮点数
arr = np.random.uniform(3,6,(2,3)) #范围3-6
print(arr)
```

    [[5.86528296 3.10828465 4.29381269]
     [3.43192952 5.64066168 4.59842537]]



```python
# 生成指定范围区间内的随机整数
arr = np.random.randint(1,10,(2,3))
print(arr)
```

    [[8 6 2]
     [1 4 6]]



```python
# 生成随机数列（正态分布）
arr = np.random.randn(2,3)
print(arr)
```

    [[-1.35886887  0.0651012  -1.65480034]
     [ 0.77452323 -0.7400233   0.29623509]]



```python
# 设置随机种子:保证数组的可复现性
np.random.seed(20)
arr = np.random.rand(2,3)
print(arr)
```

    [[0.5881308  0.89771373 0.89153073]
     [0.81583748 0.03588959 0.69175758]]


### 4.ndarray的数据类型
- bool：布尔类型
- int8\uint8：有（无）符号的8位（1字节）整型
- int16,uint16,int32,uint32,int6,uint64
- float16：半精度浮点型
- float32:单精度浮点型
- float64：双精度浮点型
- complex64：用两个32位浮点数表示的复数
- complex128：用两个64位浮点数表示的复数


```python
# bool类型
arr = np.array([1,0,2,0],dtype = 'bool') #dtype = np.bool也可以
print(arr)
```

    [ True False  True False]



```python
# 整数类型
arr = np.array([1,0,2,0],dtype = np.int8) #np.int自动调整,
print(arr)
```

    [1 0 2 0]


### 5.ndarray的操作

#### 索引与切片
- 基本索引：通过整数索引直接访问元素
- 行/列切片：使用冒号
- 连续切片：从起始索引到结束索引按步长切片
- slice函数：自定义切片规则slice(start,stop,step)
- 布尔索引：通过布尔条件删选满足条件的元素


```python
# 一维数组索引与切片
arr = np.random.randint(1,100,20)
print(arr)
```

    [97 41 86 91 27 84 17 63 17  8 99  7 27 14 76 59 26  4 75 76]



```python
# 基本索引
print(arr[0])

# 冒号
print(arr[:]) # 获取全部数据

# 连续切片
print(arr[1:5])

# slice函数(和连续切片差不多)
print(arr[slice(1,5)])

# 布尔索引
print(arr[(arr>50) & (arr<80)])
```

    97
    [97 41 86 91 27 84 17 63 17  8 99  7 27 14 76 59 26  4 75 76]
    [41 86 91 27]
    [41 86 91 27]
    [63 76 59 75 76]



```python
# 二维数组索引与切片
arr = np.random.randint(1,100,(4,4))
print(arr)
```

    [[62 78 84 58]
     [95 33 11  7]
     [76 19  4 78]
     [18 44 17 19]]



```python
# 基本索引
print(arr[2,2])

# 冒号
print(arr[:,:])

# 连续切片
print(arr[0:3,1:2])

# 布尔索引
print(arr[arr>50]) # 返回一维结果
```

    4
    [[62 78 84 58]
     [95 33 11  7]
     [76 19  4 78]
     [18 44 17 19]]
    [[78]
     [33]
     [19]]
    [62 78 84 58 95 76 78]


#### 数组的运算



```python
# 一维数组
a = np.array([1,2,3])
b = np.array([4,5,6])
```


```python
# 加
print(a+b)

# 减
print(a-b)

# 乘
print(a*b)

# 除
print(a/b)

# 幂方
print(a ** b)
```

    [5 7 9]
    [-3 -3 -3]
    [ 4 10 18]
    [0.25 0.4  0.5 ]
    [  1  32 729]



```python
# 数组与标量运算
print(a + 3)
print(a * 3)
```

    [4 5 6]
    [3 6 9]



```python
# 广播机制: 获取形状，维度补齐，元素级运算
# 相当于将下面两个数组扩展为3 * 3再进行相加

'''
a=
1 2 3
1 2 3
1 2 3

b=
4 4 4
5 5 5
6 6 6
'''

a = np.array([1,2,3]) # 1 * 3
b = np.array([[4],[5],[6]]) # 3 * 1

print(a+b)
```

    [[5 6 7]
     [6 7 8]
     [7 8 9]]



```python
# 二维数组的运算
a = np.array([[1,2,3],[4,5,6],[7,8,9]])
b = np.array([[9,8,7],[6,5,4],[3,2,1]])

# 点乘
print("a*b：",a*b)

# 叉乘
print("\na@b：",a@b)
```

    a*b： [[ 9 16 21]
     [24 25 24]
     [21 16  9]]
    
    a@b： [[ 30  24  18]
     [ 84  69  54]
     [138 114  90]]


## Numpy常用函数

#### 基本数学函数
- np.sqrt()：计算平方根，返回浮点数
- np.exp(arg)：计算自然指数$e^{arg}$
- np.log(arg)：计算自然对数$log_earg$
- np.sin()：计算正弦值
- np.cos()：计算余弦值
- np.abs()：计算绝对值
- np.power(a,b)：计算$a^b$
- np.round()：四舍五入
- np.ceil()：向上取整
- np.floor：向下取整
- np.isnan()：检测空值

#### 基本统计函数
- np.sum()：求和
- np.mean()：平均值
- np.median()：中位数
- np.var()：方差
- np.std()：标准差
- np.max()：最大值
- np.min()：最小值
- np.argmax()：最大值及其索引
- np.argmin()：最小值及其索引
- np.percentile(arr,num)：arr的num分位数
- np.cumsum()：累计和
- np.cumprod()：累计积

#### 比较函数
- np.greater(arr,num)：arr中的元素是否大于num，返回bool数组，也可传入相同大小的数组，依次比较
- np.less(arr,num)：arr中的元素是否小于num
- np.equal(arr,num)：arr中的元素是否等于num
- np.logical_and()：逻辑与
- np.logical_not()：逻辑非
- np.logical_or()：逻辑或
- np.any()：检查元素是否至少有一个元素为True
- np.all()：检查是否所有元素全是True
- np.where(condition,exe1,exe2)：满足条件执行exe1，不满足执行exe2，可以嵌套使用
- np.select(condition,result)：满足条件condition返回result，可以有多个条件和结果

#### 排序函数
- np.sort(arr)：对原数组arr排序，不改变原数组
- arr.sort：对原数组排序，改变原数组
- np.argsort(arr)：获取排序索引
- np.unique()：去重
- np.concatenate(arr1,arr2)：数组拼接
- np.split(arr,n)：将arr均分为n分（要能整除）；否则n=[a,b,c]：从a，b，c分割
- np.reshape(arr,list)：list = [a,b]，将数组重构为a行b列（要能整除）
- np.resize(arr,list)：与reshape相似，但是resize修改原数组，而reshape返回新数组

## 线性代数(linalg模块)
- np.linalg.inv(arr)：矩阵求逆
- np.linalg.det(arr)：行列式
- np.linalg.eig(arr)：特征向量与特征解
- np.linalg.solve(arr)：解线性方程组


## 文件读写
- np.save(path,arr)：存储
- np.load(path)：加载

## 练习

题目 1：温度数据分析


某城市一周的最高气温 (℃) 为 [28,30,29,31,32,30,29]。


计算平均气温、最高气温和最低气温。


找出气温超过 30℃的天数。


```python
# 定义列表
arr = np.array([28,30,29,31,32,30,29])

# 平均气温(保留两位小数)
print("平均气温为：",'%.2f'%np.mean(arr))

# 最高气温
print("最高气温为：",np.max(arr))

# 最低气温
print("最低气温为：",np.min(arr))

# 找出气温超过30的天数
print("气温超过30的天数：",len(arr[arr>30]))
```

    平均气温为： 29.86
    最高气温为： 32
    最低气温为： 28
    气温超过30的天数： 2


题目 2：学生成绩统计


某班级 5 名学生的数学成绩为 [85,90,78,92,88]。


计算成绩的平均分、中位数和标准差。


```python
arr = np.array([85,90,78,92,88])

# 计算平均分
print('平均分为：',np.mean(arr))

# 计算中位数
print('中位数为：',np.median(arr))

# 计算标准差
print('标准差为：','%.2f'%np.std(arr))
```

    平均分为： 86.6
    中位数为： 88.0
    标准差为： 4.88


题目 4：随机数据生成


生成一个（3，4）的随机整数数组，范围 [0，10）。


计算每列的最大值和每行的最小值。


将数组中的所有奇数替换为 - 1


```python
arr = np.random.randint(1,10,(3,4))
print(arr)
```

    [[8 7 7 9]
     [3 2 4 3]
     [7 5 7 5]]



```python
# 每一列最大值
print('每一列的最大值',np.max(arr,axis = 0))

# axis=0表示按沿行（竖直）方向操作，axis = 1表示沿列方向（水平）操作

# 每一行的最小值
print('每一行的最小值',np.min(arr,axis = 1))

# 将奇数替换为1
print(np.where(arr % 2 == 1,-1,arr))
```

    每一列的最大值 [8 7 7 9]
    每一行的最小值 [7 2 5]
    [[ 8 -1 -1 -1]
     [-1  2  4 -1]
     [-1 -1 -1 -1]]



```python

```
