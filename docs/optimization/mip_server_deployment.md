# 电信网络优化
## 题目
### 题目背景
在给定结构的电信网络中，为了将视频内容快速、低成本地传送到每个住户小区，需要在该网络结构中选择一些网络节点附近放置视频内容存储服务器。
### 已知条件
1. 每条链路有两个属性：最大带宽（BandwidthMax）、带宽使用成本（CostBandwidth）；
2. 每台服务器有两个属性：负荷能力（Capacity）、使用成本（CostService）；
3. 每个消费节点（对应住户小区）有明确的视频播放需求（Demand）。
### 约束要求
1. 每个节点最多部署一台服务器；
2. 每台服务器最多部署到一个节点上；
3. 必须满足所有住户小区的视频播放需求；
4. 中转节点的流量要平衡（接收总流量 = 发送总流量）。
### 优化目标
确定视频内容存储服务器的放置位置及需使用的带宽链路，使得：
1. 服务器使用总成本最小；
2. 链路使用总成本最小。

![](/images/线路图.png)
### 具体数据
```
普通节点数量：28
边数量：45
用户节点数量：12
服务器部署成本：100
服务器流量限制：50
```
#### 普通节点
| 前序节点 | 后续节点 | 最大带宽 | 每单位带宽成本 |
|----------|----------|----------|----------------|
| 0        | 16       | 8        | 2              |
| 0        | 26       | 13       | 2              |
| 0        | 9        | 14       | 2              |
| 0        | 8        | 36       | 2              |
| 0        | 7        | 25       | 2              |
| 0        | 6        | 13       | 2              |
| 0        | 1        | 20       | 1              |
| 0        | 2        | 16       | 1              |
| 0        | 3        | 13       | 1              |
| 1        | 19       | 26       | 2              |
| 1        | 18       | 31       | 2              |
| 1        | 16       | 24       | 2              |
| 1        | 15       | 16       | 2              |
| 1        | 2        | 4        | 1              |
| 1        | 3        | 11       | 1              |
| 2        | 4        | 37       | 2              |
| 2        | 25       | 24       | 2              |
| 2        | 21       | 5        | 2              |
| 2        | 20       | 2        | 2              |
| 2        | 3        | 7        | 1              |
| 3        | 19       | 24       | 2              |
| 3        | 24       | 17       | 2              |
| 3        | 27       | 26       | 2              |
| 4        | 5        | 26       | 1              |
| 4        | 6        | 12       | 1              |
| 5        | 6        | 14       | 1              |
| 8        | 21       | 36       | 5              |
| 9        | 10       | 6        | 1              |
| 9        | 11       | 14       | 1              |
| 10       | 26       | 11       | 5              |
| 10       | 11       | 9        | 1              |
| 12       | 13       | 15       | 1              |
| 12       | 14       | 9        | 1              |
| 12       | 15       | 12       | 1              |
| 13       | 14       | 11       | 1              |
| 13       | 15       | 27       | 1              |
| 14       | 15       | 19       | 1              |
| 17       | 18       | 22       | 1              |
| 21       | 22       | 22       | 1              |
| 21       | 23       | 18       | 1              |
| 21       | 24       | 14       | 1              |
| 22       | 23       | 23       | 1              |
| 22       | 24       | 11       | 1              |
| 23       | 24       | 23       | 1              |
| 26       | 27       | 19       | 1              |


#### 用户节点


| 用户节点 | 前序节点 | 节点宽带需求量 |
|----------|----------|----------------|
| 0        | 8        | 40             |
| 1        | 11       | 13             |
| 2        | 22       | 28             |
| 3        | 3        | 45             |
| 4        | 17       | 11             |
| 5        | 19       | 26             |
| 6        | 16       | 15             |
| 7        | 13       | 13             |
| 8        | 5        | 18             |
| 9        | 25       | 15             |
| 10       | 7        | 10             |
| 11       | 24       | 23             |

## 建模思路
### 一、 问题背景与参数定义

本模型旨在解决网络内容分发中的**设施选址与流分配问题**。我们需要在满足所有用户需求、且单台服务器产能受限的前提下，决策服务器部署位置和链路流量路径，使总成本最低。

此外，该方案额外扩展了**N-1 容错能力**，即任意一台已部署的服务器发生故障时，剩余系统仍能维持正常服务。

#### 1. 集合定义

* **节点集合 $V$**：包括所有网络节点 $\{0, 1, ..., 27\}$。
* **有向链路集合 $E$**：基于物理链路生成的双向有向边集合。若 $A-B$ 连通，则包含 $(A \to B)$ 和 $(B \to A)$。
* **用户集合 $K$**：挂载在特定网络节点上的消费群。

#### 2. 已知参数

* **链路参数**：对于每条有向边 $(i,j) \in E$：
    * $B_{ij}$：最大带宽限制。
    * $w_{ij}$：单位流量的传输成本。
* **节点需求 $D_i$**：
    * 节点 $i$ 上挂载的所有用户需求带宽之和。若无用户则为0。
    * $TotalDemand = \sum D_i$：全网总需求。
* **服务器参数**：
    * $C_s$：部署一台服务器的固定成本（100元）。
    * **$C_{max}$：单台服务器的最大产流能力（100单位/台）。** *(新增参数)*

---

### 二、 决策变量

1.  **服务器部署变量 ($a_i$)**：
    * $a_i \in \{0, 1\}$，$\forall i \in V$。
    * $a_i = 1$ 表示在节点 $i$ 部署服务器，否则为0。

2.  **链路流量变量 ($x_{ij}$)**：
    * $x_{ij} \ge 0$，表示链路 $(i \to j)$ 上的实际流量。

3.  **服务器产出流量 ($s_i$)**：
    * $s_i \ge 0$，表示节点 $i$ 的服务器向网络注入的流量。

---

### 三、 目标函数 (单一场景下)

在给定的约束下，最小化总成本：

$$
\min Z = \underbrace{\sum_{i \in V} (C_s \cdot a_i)}_{\text{服务器固定成本}} + \underbrace{\sum_{(i,j) \in E} (w_{ij} \cdot x_{ij})}_{\text{链路流量成本}}
$$

---

### 四、 核心约束条件

#### 1. 流量守恒约束 (Flow Conservation)

对任意节点 $i$，流入流量加上本地生产流量，必须等于流出流量加上本地消耗：

$$
\sum_{j: (j,i) \in E} x_{ji} + s_i = \sum_{j: (i,j) \in E} x_{ij} + D_i, \quad \forall i \in V
$$

#### 2. 服务器逻辑开关约束 (Big-M)

建立“部署状态”与“产出能力”的逻辑关联。如果未部署服务器 ($a_i=0$)，则产出必须为0：

$$
s_i \le TotalDemand \cdot a_i, \quad \forall i \in V
$$

#### 3. 服务器最大产能约束 (Capacity Limit)

**（代码新增逻辑）**
即便部署了服务器，单台服务器的产出也不能超过其物理极限 $C_{max}$：

$$
s_i \le C_{max}, \quad \forall i \in V
$$

> *建模提示：在数学上，约束2和约束3可以合并为更紧凑的形式 $s_i \le \min(TotalDemand, C_{max}) \cdot a_i$。但在代码中为了清晰，我们通常如上分别列出。*

#### 4. 链路带宽约束

$$
0 \le x_{ij} \le B_{ij}, \quad \forall (i,j) \in E
$$

#### 5. 最小服务器数量约束（用于迭代控制）

$$
\sum_{i \in V} a_i \ge N_{min}
$$

*其中 $N_{min}$ 是由外层算法动态调整的参数。*

---

### 五、 容错优化算法流程 (Robust Optimization Process)

由于直接在模型中加入“任意一台服务器故障”的约束会导致模型过于复杂（变成多场景随机规划），我们采用**迭代验证法**（Iterative Check）来求解：

1.  **初始化**：设定最小服务器数量 $N_{min} = 2$。
2.  **主求解**：在满足上述所有约束的前提下，求解最优部署方案（得到集合 $Deployed$）。
    * 若无解，则结束。
3.  **N-1 容错验证**：
    * 遍历集合 $Deployed$ 中的每一台服务器 $k$。
    * 假设服务器 $k$ 崩溃（强制 $s_k = 0$），其余已部署服务器保持位置不变（固定 $a_i$），重新计算流量分配。
    * 检查是否仍有可行解（即剩余服务器产能 + 链路带宽是否足够满足所有需求）。
4.  **决策与迭代**：
    * 如果**所有**单点故障测试均通过 $\rightarrow$ 输出最终方案。
    * 如果**任意**一次测试失败 $\rightarrow$ 说明当前服务器数量不足以支撑容错。
    * **更新操作**：令 $N_{min} = N_{min} + 1$，返回步骤2重新求解。

---

### 六、 模型总结

该模型通过结合**混合整数规划 (MIP)** 与 **启发式迭代算法**，实现了以下平衡：

1.  **经济性**：在正常工况下寻找成本最低的流控方案。
2.  **物理真实性**：考虑了带宽限制和服务器单机产能上限 ($C_{max}$)。
3.  **高可用性**：保证了方案具备抵抗单点故障的能力（Robustness）。
---
### 七、 详细代码及运行结果
#### 详细代码
```python
import coptpy as cp
from coptpy import COPT
from typing import List, Dict


class NetworkOptimizer:
    def __init__(self, link_data, user_data, node_count=28, server_cost=100,server_max_capacity=100):
        self.link_data = link_data
        self.user_data = user_data
        self.node_count = node_count
        self.server_cost = server_cost
        self.server_max_capacity = server_max_capacity
        self.env = cp.Envr()

        # 预处理数据
        self.V = list(range(node_count))
        self.E, self.B, self.w = self._process_links()
        self.node_demand, self.total_demand = self._process_users()

    # 读取线路数据
    def _process_links(self):
        E = []
        B = {}
        w = {}
        for i, j, b, cost in self.link_data:
            # 双向拆分
            E.append((i, j))
            B[(i, j)] = b
            w[(i, j)] = cost
            E.append((j, i))
            B[(j, i)] = b
            w[(j, i)] = cost
        return E, B, w

    # 读取用户数据
    def _process_users(self):
        d = {i: 0 for i in self.V}
        for _, node_idx, demand in self.user_data:
            d[node_idx] += demand
        return d, sum(d.values())

    # 建立模型
    def solve_scenario(self, fixed_servers: List[int] = None, failed_server: int = None, min_servers: int = 0) -> Dict:
        model = self.env.createModel(f"NetOpt")
        model.setParam(COPT.Param.Logging, 0)

        # 变量定义
        a = {i: model.addVar(vtype=COPT.BINARY, name=f"a_{i}") for i in self.V}
        x = {e: model.addVar(lb=0, ub=self.B[e], vtype=COPT.CONTINUOUS) for e in self.E}
        s = {i: model.addVar(lb=0, vtype=COPT.CONTINUOUS) for i in self.V}

        # 目标函数
        model.setObjective(
            cp.quicksum(self.server_cost * a[i] for i in self.V) + cp.quicksum(x[e] * self.w[e] for e in self.E),
            COPT.MINIMIZE
        )

        # 约束条件
        # 流量守恒
        for i in self.V:
            in_flow = cp.quicksum(x[(j, i)] for j in self.V if (j, i) in self.E)
            out_flow = cp.quicksum(x[(i, j)] for j in self.V if (i, j) in self.E)
            model.addConstr(in_flow + s[i] == out_flow + self.node_demand[i])

        # 服务器能力 (Big-M)
        for i in self.V:
            if failed_server is not None and i == failed_server:
                # 如果是崩溃节点，强制产流为0，且不计入部署变量约束
                model.addConstr(s[i] == 0)
            else:
                # 如果没有崩溃，设置服务器流量上限
                model.addConstr(s[i] <= self.server_max_capacity * a[i], name=f"ServerCap_{i}")

        # 特殊场景控制
        if fixed_servers is not None:
            # 验证模式：固定部署方案
            for i in self.V:
                if i in fixed_servers:
                    model.addConstr(a[i] == 1)
                else:
                    model.addConstr(a[i] == 0)
        else:
            # 主求解模式：限制最少数量
            if min_servers > 0:
                model.addConstr(cp.quicksum(a[i] for i in self.V) >= min_servers)

        # 4. 求解
        model.solve()

        if model.status == COPT.OPTIMAL:
            deployed = [i for i in self.V if a[i].x > 0.5]
            # 部署节点的生产流量（s[i]的值）
            server_production = {i: round(s[i].x, 2) for i in deployed}

            # 计算所有节点的输入/输出流量（用于后续验证）
            node_in_flow = {}
            node_out_flow = {}
            for i in self.V:
                # 输入流量：所有流入i的链路流量和
                node_in_flow[i] = round(cp.quicksum(x[(j, i)].x for j in self.V if (j, i) in self.E).getValue(), 2)
                # 输出流量：所有流出i的链路流量和
                node_out_flow[i] = round(cp.quicksum(x[(i, j)].x for j in self.V if (i, j) in self.E).getValue(), 2)

            scenario_name = "Normal" if failed_server is None else f"Fail_{failed_server}"
            verification_passed = self._verify_solution(a, x, s, context=scenario_name)

            if not verification_passed:
                print("严重警告：求解器报告最优，但解未通过物理约束验证！")

            return {
                "status": "Optimal",
                "obj": model.objVal,
                "deployed": deployed,
                "server_production": server_production,  # 部署节点的生产流量
                "node_in_flow": node_in_flow,  # 所有节点的输入流量
                "node_out_flow": node_out_flow,  # 所有节点的输出流量
                "total_production": round(sum(server_production.values()), 2)  # 总生产流量
            }
        else:
            return {"status": "Infeasible"}

    # 迭代寻找满足容错要求的方案
    def run_robust_optimization(self):
        # 初始最少需要2台
        min_servers_needed = 2

        while True:
            print(f"\n尝试求解：限制最少部署 {min_servers_needed} 台服务器...")

            # 求解主模型
            result = self.solve_scenario(min_servers=min_servers_needed)

            if result["status"] != "Optimal":
                print("❌ 无法找到可行解（可能带宽不足或约束冲突）。")
                break

            current_servers = result["deployed"]
            current_cost = result["obj"]
            print(f"✅ 找到候选方案: 部署在 {current_servers}, 总成本: {current_cost:.2f}")

            # 验证容错性 (N-1 校验)
            all_pass = True
            for s_node in current_servers:
                # 模拟 s_node 崩溃
                check_res = self.solve_scenario(fixed_servers=current_servers, failed_server=s_node)

                if check_res["status"] != "Optimal":
                    print(f" ⚠️ 容错测试失败: 当服务器 {s_node} 崩溃时，剩余节点无法满足需求。")
                    all_pass = False
                    break  # 只要有一个坏了不行，这套方案就废了
                else:
                    print(f"  Pass: 服务器 {s_node} 崩溃后，系统仍可运行 (替代成本: {check_res['obj']:.2f})")

            # 决策
            if all_pass:
                print("\n" + "=" * 80)
                print("🎉 最终结果：方案已通过所有单点故障测试！")
                print(f"最终部署节点: {current_servers}")
                print(f"正常运行成本: {current_cost:.2f}")
                print(f"\n部署节点生产流量:")
                for node, prod in result["server_production"].items():
                    print(f"  节点 {node}: {prod} 单位")
                print(f"\n总生产流量: {int(result['total_production'])} 单位")
                print(f"总用户需求: {self.total_demand} 单位")  # 对比总生产和总需求（理论上应相等）
                print("=" * 80)
                break
            else:
                print(f"🔄 当前方案不满足容错，增加服务器数量下限 -> {min_servers_needed + 1}")
                min_servers_needed += 1

                if min_servers_needed > len(self.V):
                    print("已遍历所有节点，无解。")
                    break

    # 验证当前解是否严格满足所有物理约束
    def _verify_solution(self, a, x, s, context="Scenario"):
        print(f"\n [{context}] 开始约束一致性校验...")
        is_valid = True
        EPS = 1e-4  # 浮点数容差

        # 1. 验证带宽约束
        for e in self.E:
            flow = x[e].x
            limit = self.B[e]
            if flow > limit + EPS:
                print(f"  ❌ 带宽超标: 链路 {e} 流量={flow:.2f} > 上限={limit}")
                is_valid = False

        # 验证服务器逻辑
        for i in self.V:
            prod = s[i].x
            deployed = a[i].x > 0.5  # 二进制变量判断

            # 未部署却产流
            if not deployed and prod > EPS:
                print(f"  ❌ 幽灵流量: 节点 {i} 未部署服务器，但产出了 {prod:.2f} 流量")
                is_valid = False

            # 产流超过单机上限
            if prod > self.server_max_capacity + EPS:
                print(f"  ❌ 产能超标: 节点 {i} 产出={prod:.2f} > 单机上限={self.server_max_capacity}")
                is_valid = False

        # 验证流量守恒 (Flow Conservation)
        # 流入 + 生产 == 流出 + 消耗
        for i in self.V:
            in_flow = sum(x[(j, i)].x for j in self.V if (j, i) in self.E)
            out_flow = sum(x[(i, j)].x for j in self.V if (i, j) in self.E)
            production = s[i].x
            consumption = self.node_demand[i]

            lhs = in_flow + production  # 总进入
            rhs = out_flow + consumption  # 总离开

            if abs(lhs - rhs) > EPS:
                print(f"  ❌ 流量不守恒 (节点 {i}):")
                print(f"     流入({in_flow:.2f}) + 生产({production:.2f}) = {lhs:.2f}")
                print(f"     流出({out_flow:.2f}) + 消耗({consumption:.2f}) = {rhs:.2f}")
                print(f"     误差: {abs(lhs - rhs):.4f}")
                is_valid = False

        if is_valid:
            print(f"  ✅ [{context}] 所有约束验证通过！(Flow, Bandwidth, Capacity)")
        else:
            print(f"  ⚠️ [{context}] 存在约束违规，请检查模型！")

        return is_valid

if __name__ == "__main__":
    # 链路数据 (起点, 终点, 带宽, 成本)
    link_data = [
        (0, 16, 8, 2), (0, 26, 13, 2), (0, 9, 14, 2), (0, 8, 36, 2), (0, 7, 25, 2), (0, 6, 13, 2),
        (0, 1, 20, 1), (0, 2, 16, 1), (0, 3, 13, 1), (1, 19, 26, 2), (1, 18, 31, 2), (1, 16, 24, 2),
        (1, 15, 16, 2), (1, 2, 4, 1), (1, 3, 11, 1), (2, 4, 37, 2), (2, 25, 24, 2), (2, 21, 5, 2),
        (2, 20, 2, 2), (2, 3, 7, 1), (3, 19, 24, 2), (3, 24, 17, 2), (3, 27, 26, 2), (4, 5, 26, 1),
        (4, 6, 12, 1), (5, 6, 14, 1), (8, 21, 36, 5), (9, 10, 6, 1), (9, 11, 14, 1), (10, 26, 11, 5),
        (10, 11, 9, 1), (12, 13, 15, 1), (12, 14, 9, 1), (12, 15, 12, 1), (13, 14, 11, 1),
        (13, 15, 27, 1), (14, 15, 19, 1), (17, 18, 22, 1), (21, 22, 22, 1), (21, 23, 18, 2),
        (21, 24, 14, 1), (22, 23, 23, 1), (22, 24, 11, 1), (23, 24, 23, 1), (26, 27, 19, 1)
    ]

    # 用户数据 (ID, 挂载节点, 需求)
    user_data = [
        (0, 8, 40), (1, 11, 13), (2, 22, 28), (3, 3, 45), (4, 17, 11), (5, 19, 26),
        (6, 16, 15), (7, 13, 13), (8, 5, 18), (9, 25, 15), (10, 7, 10), (11, 24, 23)
    ]

    # 运行优化器
    opt = NetworkOptimizer(link_data, user_data, node_count=28, server_cost=100, server_max_capacity=50)
    opt.run_robust_optimization()
```

#### 运行结果
```
尝试求解：限制最少部署 2 台服务器...

 [Normal] 开始约束一致性校验...
  ✅ [Normal] 所有约束验证通过！(Flow, Bandwidth, Capacity)
✅ 找到候选方案: 部署在 [0, 3, 5, 8, 19, 22], 总成本: 895.00
 ⚠️ 容错测试失败: 当服务器 0 崩溃时，剩余节点无法满足需求。
🔄 当前方案不满足容错，增加服务器数量下限 -> 3

尝试求解：限制最少部署 3 台服务器...

 [Normal] 开始约束一致性校验...
  ✅ [Normal] 所有约束验证通过！(Flow, Bandwidth, Capacity)
✅ 找到候选方案: 部署在 [0, 3, 5, 8, 19, 22], 总成本: 895.00
 ⚠️ 容错测试失败: 当服务器 0 崩溃时，剩余节点无法满足需求。
🔄 当前方案不满足容错，增加服务器数量下限 -> 4

尝试求解：限制最少部署 4 台服务器...

 [Normal] 开始约束一致性校验...
  ✅ [Normal] 所有约束验证通过！(Flow, Bandwidth, Capacity)
✅ 找到候选方案: 部署在 [0, 3, 5, 8, 19, 22], 总成本: 895.00
 ⚠️ 容错测试失败: 当服务器 0 崩溃时，剩余节点无法满足需求。
🔄 当前方案不满足容错，增加服务器数量下限 -> 5

尝试求解：限制最少部署 5 台服务器...

 [Normal] 开始约束一致性校验...
  ✅ [Normal] 所有约束验证通过！(Flow, Bandwidth, Capacity)
✅ 找到候选方案: 部署在 [0, 3, 5, 8, 19, 22], 总成本: 895.00
 ⚠️ 容错测试失败: 当服务器 0 崩溃时，剩余节点无法满足需求。
🔄 当前方案不满足容错，增加服务器数量下限 -> 6

尝试求解：限制最少部署 6 台服务器...

 [Normal] 开始约束一致性校验...
  ✅ [Normal] 所有约束验证通过！(Flow, Bandwidth, Capacity)
✅ 找到候选方案: 部署在 [0, 3, 5, 8, 19, 22], 总成本: 895.00
 ⚠️ 容错测试失败: 当服务器 0 崩溃时，剩余节点无法满足需求。
🔄 当前方案不满足容错，增加服务器数量下限 -> 7

尝试求解：限制最少部署 7 台服务器...

 [Normal] 开始约束一致性校验...
  ✅ [Normal] 所有约束验证通过！(Flow, Bandwidth, Capacity)
✅ 找到候选方案: 部署在 [1, 3, 5, 8, 19, 22, 25], 总成本: 927.00

 [Fail_1] 开始约束一致性校验...
  ✅ [Fail_1] 所有约束验证通过！(Flow, Bandwidth, Capacity)
  Pass: 服务器 1 崩溃后，系统仍可运行 (替代成本: 1040.00)

 [Fail_3] 开始约束一致性校验...
  ✅ [Fail_3] 所有约束验证通过！(Flow, Bandwidth, Capacity)
  Pass: 服务器 3 崩溃后，系统仍可运行 (替代成本: 1050.00)

 [Fail_5] 开始约束一致性校验...
  ✅ [Fail_5] 所有约束验证通过！(Flow, Bandwidth, Capacity)
  Pass: 服务器 5 崩溃后，系统仍可运行 (替代成本: 1017.00)

 [Fail_8] 开始约束一致性校验...
  ✅ [Fail_8] 所有约束验证通过！(Flow, Bandwidth, Capacity)
  Pass: 服务器 8 崩溃后，系统仍可运行 (替代成本: 1147.00)

 [Fail_19] 开始约束一致性校验...
  ✅ [Fail_19] 所有约束验证通过！(Flow, Bandwidth, Capacity)
  Pass: 服务器 19 崩溃后，系统仍可运行 (替代成本: 1040.00)

 [Fail_22] 开始约束一致性校验...
  ✅ [Fail_22] 所有约束验证通过！(Flow, Bandwidth, Capacity)
  Pass: 服务器 22 崩溃后，系统仍可运行 (替代成本: 1266.00)

 [Fail_25] 开始约束一致性校验...
  ✅ [Fail_25] 所有约束验证通过！(Flow, Bandwidth, Capacity)
  Pass: 服务器 25 崩溃后，系统仍可运行 (替代成本: 1000.00)

================================================================================
🎉 最终结果：方案已通过所有单点故障测试！
最终部署节点: [1, 3, 5, 8, 19, 22, 25]
正常运行成本: 927.00

部署节点生产流量:
  节点 1: 50.0 单位
  节点 3: 50.0 单位
  节点 5: 18.0 单位
  节点 8: 48.0 单位
  节点 19: 26.0 单位
  节点 22: 50.0 单位
  节点 25: 15.0 单位

总生产流量: 257 单位
总用户需求: 257 单位
================================================================================
```
---