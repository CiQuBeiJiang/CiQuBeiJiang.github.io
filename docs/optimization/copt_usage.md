# COPT下载及基础使用
## COPT介绍

## 下载流程
- 前往[官网](https://www.shanshu.ai/copt)申请求解器
![求解器截图](/images/copt.png)
- 审核通过后，会有安装包和licence发送到邮箱
![邮件截图](/images/copt1.png)
- 安装好后将邮件附带的`license.dat`和`license.key`拷贝到COPT的安装目录下，也就是拷贝到`C:\Program Files\COPT`下
- 大功告成


> 如碰到问题可以参考[用户手册](https://guide.coap.online/copt/zh-doc/quickstart.html)

## COPT基础使用方法


**以这个问题为例：**
$$
min \ Z = 3x + 5y
$$

$$
s.t. \begin{cases} 2x+y \ge 8 \\ x+2y \ge 6 \end{cases}
$$

### 类导入以及实例创建
- `Envr`类：创建一个COPT环境
- `model`类：代表优化模型，包含所有变量，约束与目标函数


```python
# 导入
import coptpy as cp
from coptpy import COPT

# 创建实例
env = cp.Envr()
model = env.createModel(name = 'model_name')
```


```
Cardinal Optimizer v8.0.2. Build date Dec  1 2025
Copyright Cardinal Operations 2025. All Rights Reserved
```  

### `model`类基本信息
- `model.status`：模型解的状态
    - COPT.Status.OPTIMAL (5)：线性规划找到全局最优解
    - COPT.Status.MIP_OPTIMAL (10)：整数规划找到全局整数最优解
    - COPT.Status.FEASIBLE (7)：找到可行解（非最优）
    - COPT.Status.MIP_FEASIBLE (11)：整数规划找到可行解（非最优）
    - COPT.Status.INFEASIBLE (2)：模型无解（约束冲突）
    - COPT.Status.UNBOUNDED (3)：模型无界解（目标函数无限优化）
    - COPT.Status.TIMEOUT (15)：模型求解超时
    - COPT.Status.LICENSEERROR (17)：许可证失效，无法求解
- `model.objval`：目标函数值（存储模型的最优目标函数值）

### 添加决策变量
- `model.addVar(lb,ub,vtype= ,name)`：添加一个单独的决策变量
    - lb：下界
    - ub：上界
    - vtype：变量的类型
        - COPT.CONTINUOUS (连续变量)
        - COPT.INTEGER (整数变量)
        - COPT.BINARY (二进制变量，即 0 或 1)
    - name：变量名称
- `model.addVars(*indices, lb, ub, obj, vtype= , nameprefix="")`：添加一组类型为tuple的变量，返回tuplelist



```python
# 添加一个决策变量
x = model.addVar(lb=0.0, ub=COPT.INFINITY, vtype=COPT.CONTINUOUS, name='x')

# 等价写法
y = model.addVar(lb=0.0, ub=cp.COPT.INFINITY, vtype=cp.COPT.CONTINUOUS, name='y')
print(x,y)
```

```
<coptpy.Var: x> <coptpy.Var: y>
```


```python
# 添加一组决策变量(2 * 3,下标从(0,0) 到(1,2))
x = model.addVars(2, 3, vtype=COPT.INTEGER, nameprefix='x')
print(x.select())
```

```
    [<coptpy.Var: x(0,0)>, <coptpy.Var: x(0,1)>, <coptpy.Var: x(0,2)>, <coptpy.Var: x(1,0)>, <coptpy.Var: x(1,1)>, <coptpy.Var: x(1,2)>]
```


### 设置目标函数
- `Model.setObjective(expr, sense=None)`
    - `expr`：表达式（必填，无默认值）
    - `sense`：指定优化方向（默认最小）
        - `cp.COPT.MINIMIZE`（求最小值）
        - `cp.COPT.MAXIMIZE`（求最大值）


```python
# 例如求3x+5y的最小值
model.setObjective(3*x + 5*y, sense=cp.COPT.MINIMIZE)
```

### 添加约束
- Model.addConstr(lhs, sense=None, rhs=None, name="")
    - `lhs`：约束的左侧表达式
    - `sense`：关系运算符
        - `cp.COPT.LESS_EQUAL`：小于等于
        - `cp.COPT.EQUAL`：等于
        - `cp.COPT.GREATER_EQUAL`：大于等于
    - `rhs`：约束的右侧表达式
- Model.addConstr(表达式)



```python
# 添加约束1
model.addConstr(2*x + 1*y,cp.COPT.GREATER_EQUAL, 8)
# 添加约束2，这种写法更简单
model.addConstr(1*x + 2*y >= 6)
```

```
<coptpy.Constraint: >
```


### 求解参数设置：
- `Model.setParam(paramname, newval)`
- `model.setParam(COPT.Param.TimeLimit, 3600)`：设置求解时间限制
- `model.setParam(COPT.Param.RelGap, 0.1)`：设置求解MIP的求解Gap
- `model.setParam(COPT.Param.LazyConstraints, 1)`：关闭延迟约束（1开启）
- `model.setParam(COPT.Param.Threads, -1)`：调用全部CPU线程求解（$\ge 1$调用固定线程数目（2/4/6））
- `model.setParam(COPT.Param.Logging, 0)`：关闭日志打印（1开启，2详细日志）
- `model.setParam(COPT.Param.Presolve, 2)`：开启高级预处理（0关闭，1低价预处理）

### 求解模型
- `model.solve`：求解模型，会输出一个日志



```python
## 求解模型
model.solve()
```

    Model fingerprint: 392e914b
    
    Using Cardinal Optimizer v8.0.2 on macOS (aarch64)
    Hardware has 10 cores and 10 threads. Using instruction set ARMV8 (30)
    Minimizing a MIP problem
    
    The original problem has:
        2 rows, 29 columns and 4 non-zero elements
        3 binaries and 18 integers
    
    Starting the MIP solver with 10 threads and 32 tasks
    
    Presolving the problem
    
    The presolved problem has:
        2 rows, 2 columns and 4 non-zero elements
        2 integers
    
    Problem info:
        Range of matrix coefficients:    [1e+00,2e+00]
        Range of rhs coefficients:       [6e+00,8e+00]
        Range of bound coefficients:     [6e+00,8e+00]
        Range of cost coefficients:      [3e+00,5e+00]
        Density of cost:                     100.0%
    
         Nodes    Active  LPit/n  IntInf     BestBound  BestSolution     Gap   Time
             0         1      --       0  0.000000e+00            --     Inf  0.01s
    H        0         1      --       0  0.000000e+00  5.800000e+01 100.00%  0.01s
    H        0         1      --       0  0.000000e+00  2.300000e+01 100.00%  0.01s
    H        0         1      --       0  0.000000e+00  1.700000e+01 100.00%  0.01s
             0         1      --       2  1.666667e+01  1.700000e+01  1.961%  0.01s
             1         0     0.0       2  1.700000e+01  1.700000e+01  0.000%  0.01s
             1         0     0.0       2  1.700000e+01  1.700000e+01  0.000%  0.02s
    
    Best solution   : 17.000000000
    Best bound      : 17.000000000
    Best gap        : 0.0000%
    Solve time      : 0.02
    Solve node      : 1
    MIP status      : solved
    Solution status : integer optimal (relative gap limit 0.0001)
    
    Violations      :     absolute     relative
        bounds      :            0            0
        rows        :            0            0
        integrality :            0


### 输出解的值和变量名
-  `model.objval`：输出目标值
-  `Model.getVars()`:获得模型的所有变量；
-  `var.index`：获得变量的index，这个不同于变量名，只是一个序号；
-  `var.x`: 获得变量`var`在最优解中的取值；
-  `var.getName()`: 获得变量名。


```python
model.getVars()
print(f"x的取值为：{x.x}，y的取值为{y.x}，最小值为{model.objval}")
```plaintext

    x的取值为：4.0，y的取值为1.0，最小值为17.0


### 完整示例


```python
# 完整求解示例：min 3x+5y，s.t. 2x+y≥8, x+2y≥6, x,y≥0
import coptpy as cp
from coptpy import COPT

# 1. 创建环境与模型
env = cp.Envr()
model = env.createModel(name='LP_example')

# 2. 添加决策变量
x = model.addVar(lb=0.0, ub=COPT.INFINITY, vtype=COPT.CONTINUOUS, name='x')
y = model.addVar(lb=0.0, ub=COPT.INFINITY, vtype=COPT.CONTINUOUS, name='y')

# 3. 设置目标函数：最小化 3x+5y
model.setObjective(3*x + 5*y, sense=COPT.MINIMIZE)

# 4. 添加约束条件
model.addConstr(2*x + y >= 8, name='c1')
model.addConstr(x + 2*y >= 6, name='c2')

# 5. 求解模型
model.solve()

print("当前求解状态码：", model.status)
print("最优目标函数值：", model.objval)
print("x的最优解：", x.x)
print("y的最优解：", y.x)

# 标准判断
if model.status == 1:  # 状态码=1 → 最优解
    print("求解成功：找到全局最优解！")
    print(f"最优解：x = {x.x:.4f}, y = {y.x:.4f}")
    print(f"最优目标函数值 = {model.objval:.4f}")
elif model.status == 2:
    print("求解失败：模型无解（约束条件冲突）")
elif model.status == 3:
    print("求解失败：模型无界（目标函数可无限优化）")
else:
    print(f"求解状态：{model.status}，非最优解")
```

```

    Cardinal Optimizer v8.0.2. Build date Dec  1 2025
    Copyright Cardinal Operations 2025. All Rights Reserved
    
    Model fingerprint: c5b184a2
    
    Using Cardinal Optimizer v8.0.2 on macOS (aarch64)
    Hardware has 10 cores and 10 threads. Using instruction set ARMV8 (30)
    Minimizing an LP problem
    
    The original problem has:
        2 rows, 2 columns and 4 non-zero elements
    The presolved problem has:
        2 rows, 2 columns and 4 non-zero elements
    
    Starting the simplex solver using up to 8 threads
    
    Problem info:
        Range of matrix coefficients:    [1e+00,2e+00]
        Range of rhs coefficients:       [6e+00,8e+00]
        Range of bound coefficients:     [0e+00,0e+00]
        Range of cost coefficients:      [3e+00,5e+00]
    
    Method   Iteration           Objective  Primal.NInf   Dual.NInf        Time
    Dual             0    0.0000000000e+00            2           0       0.00s
    Dual             2    1.6667181196e+01            0           0       0.00s
    
    Solving finished
    Status: Optimal  Objective: 1.6666666667e+01  Iterations: 2  Time: 0.00s
    当前求解状态码： 1
    最优目标函数值： 16.66666666666667
    x的最优解： 3.333333333333333
    y的最优解： 1.333333333333334
    求解成功：找到全局最优解！
    最优解：x = 3.3333, y = 1.3333
    最优目标函数值 = 16.6667
```