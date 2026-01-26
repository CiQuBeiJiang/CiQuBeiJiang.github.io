# NumPy 深度指南：从入门到实战

## 1. 核心概述

NumPy (Numerical Python) 是 Python 科学计算的基石。它不仅提供了一个高性能的 `ndarray`（N-dimensional array）对象，还定义了整个数据科学生态（如 Pandas, Scikit-learn）的标准。

### 为什么选择 NumPy 而非 Python List？

- **内存布局**：ndarray 存储在连续的内存块中，而 Python List 存储的是指针的列表。

- **计算效率**：底层由 C 语言编写，支持 SIMD（单指令多数据）向量化运算，避免了 Python 层面的显式循环。

- **生态兼容**：它是 Pandas、Matplotlib、PyTorch 等库的底层依赖。

## 2. ndarray 对象详解

### 核心属性一览

| 属性       | 解释           | 示例 / 备注                         |
| ---------- | -------------- | ----------------------------------- |
| `ndim`     | 维度数量 (秩)  | 0=标量, 1=向量, 2=矩阵              |
| `shape`    | 数组形状       | `(3, 4)` 表示3行4列                 |
| `size`     | 元素总数       | 等于 shape 中数值的乘积             |
| `dtype`    | 数据类型       | 如 `int64`, `float32`（同质性要求） |
| `itemsize` | 单个元素字节数 | `float64` 为 8 字节                 |
| `nbytes`   | 总内存占用     | `size * itemsize`                   |

### 数组创建的最佳实践

#### 1. 从 Python 结构转换

```Python
import numpy as np

# 自动推断类型
arr = np.array([1, 2, 3]) 

# 强制指定类型（常用技巧：节省内存）
# 使用 float32 替代 float64 可节省一半内存
arr_f = np.array([1, 2, 3], dtype=np.float32) 
```

#### 2. 占位符生成 (初始化)

```Python
# 0填充：常用于初始化权重或容器
zeros = np.zeros((3, 3)) 

# 1填充：常用于乘法初始值
ones = np.ones((2, 5), dtype=int)

# 垃圾值填充：速度最快，仅分配内存不初始化（慎用）
empty = np.empty((2, 2)) 

# 指定值填充
full = np.full((3, 3), fill_value=3.14)
```

#### 3. 数值范围生成

```Python
# 等差数列：[start, stop) 左闭右开
range_arr = np.arange(0, 10, 2)  # [0, 2, 4, 6, 8]

# 线性等分：常用于绘图坐标轴生成
# 0到10之间生成5个点，包含终点
lin_arr = np.linspace(0, 10, 5)  # [0. , 2.5, 5. , 7.5, 10. ]

# 对数等分
log_arr = np.logspace(0, 2, 3)   # [1., 10., 100.] (10^0 到 10^2)
```

#### 4. 随机数生成 (Random State)

```Python
# 设定随机种子（复现实验结果的关键）
np.random.seed(42)

# 均匀分布 [0, 1)
rng_uniform = np.random.rand(3, 3)

# 标准正态分布 (均值0，方差1)
rng_normal = np.random.randn(3, 3)

# 指定范围整数 [low, high)
rng_int = np.random.randint(0, 10, (2, 2))
```

## 3. 索引与切片 (Indexing & Slicing)

⚠️ **关键概念：视图 (View) vs 副本 (Copy)**

- 切片 (Slicing)：返回原数组的视图。修改切片结果会改变原数组！

- 花式索引 (Fancy Indexing)：返回原数组的副本。修改结果不会影响原数组。

```Python
arr = np.arange(10)

# 切片 - 视图
subset = arr[0:5]
subset[:] = 99
# arr 变成了 [99, 99, 99, 99, 99, 5, 6, 7, 8, 9]

# 布尔索引 - 副本
mask_arr = arr[arr > 50] # 选出大于50的数
mask_arr[:] = 0          # 修改这个副本
# arr 保持不变，还是有很多99
```

### 多维操作技巧

```Python
matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

# 逗号分隔维度：[行处理, 列处理]
# 取第2行，第3列的元素
val = matrix[1, 2] # 6

# 取前两行，所有列
sub_matrix = matrix[:2, :] 

# 降维切片 vs 保持维度
print(matrix[:, 1].shape)  # (3,)  获得一个向量
print(matrix[:, 1:2].shape) # (3, 1) 获得一个列向量（矩阵）
```

## 4. 广播机制 (Broadcasting)

广播是 NumPy 最强大的特性之一，它允许不同形状的数组进行数学运算。

### 广播三原则

1. 对齐：如果两个数组维度不同，维度较小的数组会在其左侧补1。

2. 扩展：如果两个数组在某个维度上的大小不同，但其中一个大小为1，则该维度会被拉伸（复制）以匹配另一个数组。

3. 报错：如果以上都不满足，则抛出 ValueError。

### 实战案例：矩阵去均值

```Python
data = np.array([[1, 2, 3], 
                 [4, 5, 6], 
                 [7, 8, 9]]) # Shape (3, 3)

means = np.mean(data, axis=0) # Shape (3,) -> 广播对齐为 (1, 3) -> 拉伸为 (3, 3)

# 每一列都减去了该列的平均值
centered_data = data - means 
```

## 5. 维度操作与轴 (Axis)

理解 `axis` 对于统计计算至关重要。想象 `axis` 是我们要**压扁（Collapse）**的方向。

- `axis=0`：沿着行（垂直）方向操作 → 结果体现了列的特征。

- `axis=1`：沿着列（水平）方向操作 → 结果体现了行的特征。

```Python
arr = np.random.randint(1, 10, (3, 4))

# 计算每一列的最大值 (消灭了行维度)
col_max = np.max(arr, axis=0) 

# 计算每一行的平均值 (消灭了列维度)
row_mean = np.mean(arr, axis=1)
```

## 6. 常用函数速查表

### 统计与数学

| 函数                              | 说明     | 备注                    |
| --------------------------------- | -------- | ----------------------- |
| `np.sum` / `mean` / `std` / `var` | 基础统计 | 可指定 axis             |
| `np.min` / `max`                  | 极值     |                         |
| `np.argmin` / `argmax`            | 极值索引 | 返回最大/小值所在的位置 |
| `np.cumsum` / `cumprod`           | 累积计算 | 时间序列分析常用        |
| `np.unique`                       | 去重     | 可返回计数和索引        |

### 逻辑运算

| 函数                   | 说明             | 示例                     |
| ---------------------- | ---------------- | ------------------------ |
| `np.where(cond, x, y)` | 向量化三元表达式 | `np.where(arr>0, 1, -1)` |
| `np.any` / `np.all`    | 存在/全称量词    | 检测是否存在 True        |

### 形状变换

| 函数                    | 说明     | 备注                                         |
| ----------------------- | -------- | -------------------------------------------- |
| `reshape`               | 改变形状 | 元素总数必须一致                             |
| `flatten` / `ravel`     | 展平数组 | `ravel` 返回视图（更快），`flatten` 返回副本 |
| `transpose` / `T`       | 转置     | 交换维度                                     |
| `concatenate` / `stack` | 拼接     | 注意 axis 的选择                             |

## 7. 实战练习优化

### 题目 1：气温数据分析

**场景**：某城市一周气温为 `[28, 30, 29, 31, 32, 30, 29]`。  

**任务**：

1. 计算统计指标。

2. 进阶：找出气温异常（例如超过30度）的具体日期索引。

```Python
temps = np.array([28, 30, 29, 31, 32, 30, 29])

# 1. 基础统计
print(f"平均温: {temps.mean():.2f}℃")
print(f"温差范围: {temps.ptp()}℃") # ptp = max - min

# 2. 布尔掩码
high_temps = temps[temps > 30]
print(f"高温天气数: {len(high_temps)}天")

# 3. 获取索引 (哪几天高温？)
# np.where 返回的是 tuple，需要取 [0]
high_temp_days = np.where(temps > 30)[0] 
print(f"高温出现在第 {high_temp_days + 1} 天")
```

### 题目 2：图像数据模拟（三维数组）

**场景**：模拟一张 4x4 像素的彩色图片（RGB 3通道）。  

**任务**：将所有“红色通道”大于 5 的像素点置为 0（去噪）。

```Python
# 形状：(高度, 宽度, 通道数)
img = np.random.randint(0, 10, (4, 4, 3))

# 红色通道是 index 0
red_channel = img[:, :, 0]

# 使用布尔索引修改原数组
# 逻辑：找出红色通道大于5的位置，将该位置在所有通道的值都设为0（也就是变黑）
mask = img[:, :, 0] > 5
img[mask] = 0

print("处理后的图像矩阵形状:", img.shape)
```