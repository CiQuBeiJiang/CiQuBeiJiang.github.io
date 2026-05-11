# 电信网络弹性预测性维护：XGBoost 与 MIP 联合优化框架

!!! abstract "项目摘要"

本项目针对电信基础设施老化问题，提出了一种**“预测+决策”的闭环框架**：

1. 预测层：利用 XGBoost 预测设备在未来各时间窗的故障概率（Probabilistic Prediction）。

2. 决策层：构建混合整数规划（MIP）模型，在满足网络弹性（Resilience）约束的前提下，统筹固定调度成本与故障风险，实现维护任务的智能“批处理”。

**核心成果**：相比传统策略，总成本降低 **3.4%**，调度频率降低 **50%** [cite: 4]。

## 1. 业务痛点与问题定义

在实际运维中，核心矛盾体现在两方面：

- **成本矛盾**：固定出勤费（Dispatch Cost）很高。坏一台修一台（反应式）会导致出勤费激增；定期修（预防性）又会浪费设备剩余寿命。

- **约束矛盾**：电信网络要求高可用性（例如：任意时刻必须有 85% 的节点在线）。

**目标**：找到调度方案  $x_{i,t}$ ，在保证网络韧性约束的前提下，最小化（维修费 + 出勤费 + 风险惩罚）总成本。

## 2. 模块一：基于 XGBoost 的故障概率预测

### 2.1 特征工程 (Rolling Features)

单纯的传感器读数存在噪声，为捕捉设备退化趋势，引入**滚动窗口（Rolling Window）** 特征是提高预测精度的关键。

```Python

# 核心代码截取自 Xg.py
def process_data(df, is_test=False, true_rul=None):
    # ... 基础清理 ...
    
    # 关键点：不仅看当前值，更要看过去一段时间的均值和波动率
    # capture the trend over a window of 5 cycles
    df_rolled = df.groupby('unit_number')[cols_normalize].rolling(window=5, min_periods=1).mean()
    df_rolled.columns = [f"{c}_mean" for c in cols_normalize]
    
    df_std = df.groupby('unit_number')[cols_normalize].rolling(window=5, min_periods=1).std().fillna(0)
    df_std.columns = [f"{c}_std" for c in cols_normalize]
    
    # 将原始特征、滚动均值、滚动标准差合并
    df_feat = pd.concat([df, df_rolled, df_std], axis=1)
    return df_feat
```

!!! note "为什么这样做？"

实验表明，引入滚动特征后虽有轻微滞后，但模型对长期退化趋势的捕捉更准确。对优化器而言，“设备正在变坏”的趋势信息比“设备实时数值”更有价值。

### 2.2 概率输出

传统回归模型预测剩余寿命（RUL）具体数值，本项目将其转化为多分类问题，输出每个设备在未来每个时间窗（Bin）失效的概率。

```Python

# 模型训练参数 (Xg.py)
model = xgb.XGBClassifier(
    objective='multi:softprob',  # 关键：输出多分类的概率矩阵
    num_class=len(CONFIG['rul_bins']) - 1, 
    # ... 其他参数 ...
)

# 输出结果：Prob_Matrix (N_units x T_windows)
# 这是一个 (100, 6) 的矩阵，表示100台设备在未来6个时间段的风险
prob_matrix = model.predict_proba(X_test)
```

## 3. 模块二：基于 MIP 的运筹优化决策

拿到概率矩阵后，使用 COPT (Cardinal Optimizer) 求解器进行核心决策。

### 3.1 数学建模

将业务逻辑转化为数学公式是项目核心，以下是完整建模逻辑：

#### 符号定义

-  $i∈{1..N}$ : 设备编号

-  $t∈{1..T}$ : 时间窗

-  $P_{i,t}$ : 设备  $i$  在时间  $t$  的故障概率（来自 XGBoost）

#### 决策变量

-  $x_{i,t}∈{0,1}$ : 状态变量。1 表示设备正常工作，0 表示正在维护。

-  $y_{t}∈{0,1}$ : 调度变量。1 表示时间窗  $t$  派遣运维团队（产生固定成本），0 表示未派遣。

#### 目标函数 (Objective)

 $$
 \min Z = \sum_{t} C_{fix} \cdot y_t + \sum_{i,t} \left( C_{var} \cdot (1-x_{i,t}) + C_{risk} \cdot P_{i,t} \cdot x_{i,t} \right)
 $$ 

其中：

-  $C_{fix} \cdot y_t$ ：固定调度费

-  $C_{var} \cdot (1-x_{i,t})$ ：变动维修费

-  $C_{risk} \cdot P_{i,t} \cdot x_{i,t}$ ：风险惩罚

#### 核心约束

1. **韧性约束 (Resilience Constraint)**：

     $$
     \sum_{i} x_{i,t} \geq N_{req}, \forall t
     $$

    解读：任意时间，正常工作的设备数量不能少于  $N_{req}$ （如85台）。

2. **调度逻辑关联 (Big-M Constraint)**：

     $$
     \sum_{i} (1-x_{i,t}) \leq M \cdot y_t, \forall t
     $$

    解读：若  $y_t=0$ （未派遣团队），则  $\sum(1-x)$  必须为0（无设备维修）；仅派遣团队后，才可开展维修，这是“批处理”效应的数学根源。

### 3.2 代码实现

```Python

# 核心代码截取自 diff_model.py -> solve_optimization 函数

def solve_optimization(resilience=None, ...):
    env = Envr()
    model = env.createModel("MIP_Solver")
    
    # 1. 定义变量
    x = {} # 状态变量
    y = {} # 调度变量 (Dispatch)
    for t in range(T):
        y[t] = model.addVar(vtype=COPT.BINARY) 
        for i in range(N):
            x[i, t] = model.addVar(vtype=COPT.BINARY)

    # 2. 构建目标函数
    obj = 0
    for t in range(T):
        obj += D * y[t]  # Fixed Dispatch Cost (关键成本项)
        for i in range(N):
            # 维护成本 + 风险期望成本
            obj += CONFIG['cost_maint'] * (1 - x[i, t]) + P * PROBS[i, t] * x[i, t]
    model.setObjective(obj, COPT.MINIMIZE)

    # 3. 添加约束
    for t in range(T):
        # 约束A: 网络韧性 (Resilience)
        model.addConstr(sum(x[i, t] for i in range(N)) >= R)

        # 约束B: 逻辑关联 (Big-M)
        # 统计当前维修数量
        maint_count = sum(1 - x[i, t] for i in range(N))
        # 如果没派车(y=0)，maint_count必须为0
        model.addConstr(maint_count <= N * y[t]) 

    model.solve()
    # ...
```

## 4. 关键机制分析：它是如何省钱的？

通过 `diff_model.py` 中 `run_exp4_gantt()` 可视化对比验证模型有效性：

### 4.1 批处理效应 (Batching Effect)

- **启发式策略**：“打地鼠”模式，设备风险高就修，导致每个时间窗  $y_t$  均为1，固定出勤成本极高。

- **优化策略（MIP）**：全局规划，若某时间窗需维修部分高风险设备，会将其他中风险设备合并维修，利用同一趟出勤完成多台设备维护。

结果：将分散在6个时间窗的任务压缩至2个时间窗完成，大幅降低固定出勤成本。

### 4.2 韧性与鲁棒性

通过 `run_exp2_sensitivity()` 测试  $N_{req}$  从70到95的变化：

-  $N_{req} ≤85$  时，模型成本控制游刃有余；

-  $N_{req} ≥90$ （高压环境）时，启发式策略成本突变爆炸，而MIP模型通过精细调度，成本上升平缓，极端工况下稳定性更强。

## 5. 项目复盘与自我思考

!!! tip "Self-Reflection"

Q: 这个项目的核心壁垒是什么？

A: 不是 XGBoost 也不是 COPT，而是将二者结合的 Problem Formulation（问题构建）。

大多数预测性维护仅停留在“预测设备会坏”，本项目进一步解决“在资源有限、出勤费昂贵、需保证85%在线率的前提下，具体该哪天修？哪几台一起修？”的问题。

这将单纯的**技术问题（Prediction）** 升维为**管理决策问题（Decision Making）**，也是数据科学在工业界落地的核心价值。

📎 附录：环境依赖

- Python 3.8+

- coptpy: 杉数科技求解器 (需申请 License 否则功能受限)

- xgboost: 梯度提升树库

- pandas, numpy: 数据处理

### 结果

![Strategy_Comparison.png](/images/Fig1_Strategy_Comparison.png)

![Resilience_Sensitivity.png](/images/Fig2_Resilience_Sensitivity.png)

![Pareto_Frontier.png](/images/Fig3_Pareto_Frontier.png)

![Schedule_Gantt.png](/images/Fig4_Schedule_Gantt.png)

### 总结

1. 项目核心是“预测+决策”闭环：XGBoost 输出故障概率矩阵，MIP 模型基于概率实现维护任务的全局优化调度。

2. 滚动窗口特征提升了故障概率预测的趋势捕捉能力，是预测层的关键优化点。

3. MIP 模型的“批处理”逻辑和韧性约束，是实现成本降低、调度频率减半的核心机制，体现了从技术预测到业务决策的价值升维。
