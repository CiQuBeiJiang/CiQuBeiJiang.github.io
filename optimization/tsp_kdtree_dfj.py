import coptpy as cp
from coptpy import COPT
import numpy as np
import time
import matplotlib.pyplot as plt
from scipy.spatial import KDTree
from collections import defaultdict
import warnings
# 忽略无关警告
warnings.filterwarnings('ignore')

class TSPSolver:
    def __init__(self, filename):
        self.filename = filename
        self.co_dict = None
        self.coords = None
        self.dist_matrix = None
        self.n = 0
        self.k = 15
        self.EWtype = "EUC_2D"


    # 读取数据
    def read_data(self):
        start_read = time.time()
        try:
            with open(self.filename, 'r') as f:
                lines = f.readlines()
            nodes = []
            start_collect = False
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                if 'EDGE_WEIGHT_TYPE' in line:
                    self.EWtype = line.split(':')[1].strip()
                elif 'NODE_COORD_SECTION' in line:
                    start_collect = True
                    continue
                elif 'EOF' in line:
                    break
                elif start_collect:
                    parts = line.split()
                    # 确保是合法坐标（节点编号 X Y）
                    if len(parts) == 3:
                        nodes.append([float(parts[1]), float(parts[2])])
                    else:
                        print(f"编号{parts[0]}缺少数据")

            self.n = len(nodes)
            self.coords = np.array(nodes)
            # 自适应确定k值
            self.k = self._adaptive_k()
            end_read = time.time()
            print(f"读取数据耗时: {end_read - start_read:.4f} 秒")
            print(f"K值取{self.k}")
            print(f"数据处理完成，共有{self.n}条数据")
            print(f"自动识别距离类型：EDGE_WEIGHT_TYPE = {self.EWtype}")
            return True

        except Exception as e:
            print(f"错误：读取文件失败，{str(e)}")
            return False

    def _adaptive_k(self):
        """自适应确定k值"""
        if self.n <= 50:
            return 8
        elif self.n <= 100:
            return 10
        elif self.n <= 200:
            return 12
        elif self.n <= 300:
            return 15
        elif self.n <= 400:
            return 18
        elif self.n <= 500:
            return 20
        elif self.n <= 1000:
            return 25
        elif self.n <= 2000:
            return 30
        else:
            return 35

    # 构建距离矩阵
    def construct_dist_matrix(self):
        start_dist = time.time()
        if self.EWtype == "EUC_2D":
            # 使用向量化的欧几里得距离计算
            diff = self.coords[:, np.newaxis, :] - self.coords[np.newaxis, :, :]
            self.dist_matrix = np.sqrt(np.sum(diff ** 2, axis=2))
            self.dist_matrix = np.round(self.dist_matrix, 4)

        elif self.EWtype == "MAN_2D":
            # 曼哈顿距离
            diff = self.coords[:, np.newaxis, :] - self.coords[np.newaxis, :, :]
            self.dist_matrix = np.sum(np.abs(diff), axis=2)

        elif self.EWtype == "GEOM":
            # 几何距离
            diff = self.coords[:, np.newaxis, :] - self.coords[np.newaxis, :, :]
            self.dist_matrix = np.sqrt(np.sum(diff ** 2, axis=2))
            self.dist_matrix = np.round(self.dist_matrix)

        else:
            # 默认欧几里得距离
            diff = self.coords[:, np.newaxis, :] - self.coords[np.newaxis, :, :]
            self.dist_matrix = np.sqrt(np.sum(diff ** 2, axis=2))

        # 转换为列表形式
        dist_list = self.dist_matrix.tolist()

        end_dist = time.time()
        print(f"构建距离矩阵耗时: {end_dist - start_dist:.4f} 秒")
        return dist_list

    # KDTree近邻查找
    def get_k_neighbors_kdtree(self, k=None):
        if k is None:
            k = self.k
        # k不超过节点数
        k = min(k, self.n - 1)
        # k至少为2
        k = max(k, 2)

        start_kdtree = time.time()

        tree = KDTree(self.coords)
        distances, indices = tree.query(self.coords, k = k + 1)

        # 构建近邻集合
        neighbor_sets = [set(indices[i, 1:]) for i in range(self.n)]

        # 双向近邻
        n = self.n
        for i in range(n):
            neighbors_i = neighbor_sets[i]
            for j in list(neighbors_i):
                neighbor_sets[j].add(i)

        # 限制近邻数
        for i in range(n):
            if len(neighbor_sets[i]) > k * 2:  # 双向连接可能使邻居数增加
                neighbor_sets[i] = set(list(neighbor_sets[i])[:k * 2])

        # 转换为排序列表
        neighbor_matrix = [sorted(s) for s in neighbor_sets]

        end_kdtree = time.time()
        print(f"KDTree构建邻居矩阵耗时: {end_kdtree - start_kdtree:.4f} 秒")
        return neighbor_matrix

    # 求解函数
    def solve_tsp(self):
        start_total = time.time()
        # 读取数据
        if not self.read_data():
            return None, None, None, None

        # 构建距离矩阵
        dist_matrix = self.construct_dist_matrix()

        # 使用KDTree构建邻居矩阵
        neighbor_matrix = self.get_k_neighbors_kdtree()

        # 调用DFJ求解
        model, obj_val, route, active_edges = self.DFJ_solver(dist_matrix, neighbor_matrix)

        end_total = time.time()
        time_total = end_total - start_total

        print(f"总求解时间: {time_total:.2f}秒")
        return model, obj_val, route, active_edges, time_total

    # DFJ算法求解器
    def DFJ_solver(self, dist, neighbor_matrix):
        start_dfj = time.time()
        n = self.n

        env = cp.Envr()
        model = env.createModel('TSP_DFJ')
        model.setObjective(COPT.MINIMIZE)

        # 优化参数设置
        model.setParam(COPT.Param.LazyConstraints, 1)
        model.setParam(COPT.Param.Threads, -1)
        model.setParam(COPT.Param.Logging, 0)
        model.setParam(COPT.Param.TimeLimit, 3600)
        model.setParam(COPT.Param.Presolve, 2)

        # 创建变量
        x = {}
        edge_count = 0
        for i in range(n):
            for j in neighbor_matrix[i]:
                if i < j:  # 避免重复
                    x[(i, j)] = model.addVar(
                        vtype=COPT.BINARY,
                        name=f"x_{i}_{j}",
                        obj=float(dist[i][j])
                    )
                    edge_count += 1

        print(f"创建了{edge_count}个变量（稀疏化率: {(edge_count / (n * (n - 1) / 2)) * 100:.1f}%）")

        # 度约束
        for i in range(n):
            edges = []
            for j in neighbor_matrix[i]:
                if i < j:
                    edges.append(x[(i, j)])
                elif j < i and (j, i) in x:
                    edges.append(x[(j, i)])

            if edges:
                model.addConstr(cp.quicksum(edges) == 2, name=f"degree_{i}")

        # 迭代消除子回路
        max_iter = 50
        solution_found = False

        for iteration in range(max_iter):
            print(f"\n--- 迭代 {iteration} ---")
            model.solve()

            status_map = {
                COPT.OPTIMAL: "OPTIMAL",
                COPT.INFEASIBLE: "INFEASIBLE",
                COPT.UNBOUNDED: "UNBOUNDED",
                COPT.TIMEOUT: "TIMEOUT",
                COPT.NODELIMIT: "NODE LIMIT",
                6: "FEASIBLE"  # 可行解
            }

            print(f"求解状态: {model.status} ({status_map.get(model.status, 'UNKNOWN')})")

            if model.status not in [COPT.OPTIMAL, 6]:
                break

            # 获取当前解
            x_val = np.zeros((n, n), dtype=bool)
            for (i, j) in x:
                if x[(i, j)].X > 0.5:
                    x_val[i, j] = True
                    x_val[j, i] = True

            # 快速检测子回路
            subtours = self._fast_find_subtours(x_val)

            if not subtours:
                print(f"迭代 {iteration}: 无子回路，找到可行解")
                solution_found = True
                break

            print(f"发现 {len(subtours)} 个子回路")

            # 批量添加约束
            constraints_added = 0
            for s in subtours:
                if 2 <= len(s) < n:
                    # 快速计算子回路中的边
                    edges_in_subtour = []
                    s_set = set(s)
                    for i in s:
                        for j in neighbor_matrix[i]:
                            if j in s_set and i < j:
                                edges_in_subtour.append(x[(i, j)])

                    if edges_in_subtour:
                        model.addLazyConstr(
                            cp.quicksum(edges_in_subtour) <= len(s) - 1,
                            name=f"subtour_{iteration}_{constraints_added}"
                        )
                        constraints_added += 1

            print(f"添加了 {constraints_added} 个子回路约束")

        # 提取结果
        route = []
        obj_val = None

        if solution_found or model.status in [COPT.OPTIMAL, 6]:
            obj_val = round(model.ObjVal, 4)

            # 构建邻接表
            active_edges = [[] for _ in range(n)]
            for (i, j) in x:
                if x[(i, j)].X > 0.5:
                    active_edges[i].append(j)
                    active_edges[j].append(i)

            # 构建路径
            route = self._build_route(active_edges)

            if route:
                print(f"求解成功！最优总路程 = {obj_val}")
            else:
                print("路径构建失败")

        end_dfj = time.time()
        print(f"DFJ算法求解耗时: {end_dfj - start_dfj:.4f} 秒")

        return model, obj_val, route, active_edges

    # 并查集检测子回路
    def _fast_find_subtours(self, x_val):
        n = self.n
        parent = list(range(n))
        size = [1] * n

        def find(x):
            # 路径压缩优化
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]

        def union(x, y):
            root_x = find(x)
            root_y = find(y)
            if root_x != root_y:
                # 按秩合并
                if size[root_x] < size[root_y]:
                    root_x, root_y = root_y, root_x
                parent[root_y] = root_x
                size[root_x] += size[root_y]

        # 只遍历上三角矩阵
        row_indices, col_indices = np.where(np.triu(x_val))
        for i, j in zip(row_indices, col_indices):
            union(i, j)

        # 使用字典收集分量
        components = defaultdict(list)
        for i in range(n):
            components[find(i)].append(i)

        # 过滤出子回路
        subtours = []
        for comp in components.values():
            if 2 <= len(comp) < n:
                subtours.append(comp)

        return subtours

    # 构建路径
    def _build_route(self, active_edges):
        n = self.n

        # 验证度约束
        invalid_nodes = [i for i in range(n) if len(active_edges[i]) != 2]
        if invalid_nodes:
            print(f"警告：以下节点度不为2: {invalid_nodes[:10]}{'...' if len(invalid_nodes) > 10 else ''}")
            return []

        # 尝试从不同节点开始构建路径
        for start in range(min(10, n)):
            current = start
            prev = -1
            route = []
            visited = [False] * n

            for _ in range(n):
                if visited[current]:
                    break  # 出现循环，尝试下一个起点
                visited[current] = True
                route.append(current + 1)

                neighbors = active_edges[current]
                if len(neighbors) != 2:
                    break

                # 找到下一个未访问的邻居
                next_node = None
                for neighbor in neighbors:
                    if neighbor != prev and not visited[neighbor]:
                        next_node = neighbor
                        break

                if next_node is None:
                    # 回到起点形成闭合回路
                    if current in active_edges[start] and len(route) == n:
                        route.append(start + 1)
                        return route
                    else:
                        break
                prev, current = current, next_node

            # 检查是否形成完整回路
            if (len(route) == n and
                    current == start and
                    route[0] - 1 in active_edges[route[-2] - 1]):
                route.append(start + 1)
                return route

        print("警告：无法构建完整路径")
        return []


# 绘图和验证
def plot_tsp_route(co_dict, route, obj_val, time_total, k=None):
    n = len(co_dict)

    figsize= (20, 12) if n > 500 else (16, 12)
    plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'sans-serif']
    plt.rcParams['axes.unicode_minus'] = False

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize, gridspec_kw={'width_ratios': [8, 2]})

    # 左图：路线图
    x_coords = []
    y_coords = []
    for node_id in route:
        x, y = co_dict[node_id]
        x_coords.append(x)
        y_coords.append(y)

    ax1.plot(x_coords, y_coords, 'b-', linewidth=1.2, alpha=0.7)
    ax1.scatter(x_coords, y_coords, c='r', s=15, zorder=5)
    ax1.scatter(x_coords[0], y_coords[0], c='g', s=100, marker='*', zorder=10)

    offset = 0.4  # 偏移量
    for i, (x, y) in enumerate(zip(x_coords, y_coords)):
        node_num = str(route[i])
        if i % 2 == 1:
            ax1.text(x - offset, y + offset, node_num, fontsize=9, ha='right', va='bottom', zorder=20)
        else:
            ax1.text(x + offset, y + offset, node_num, fontsize=9, ha='right', va='top', zorder=20)

    ax1.set_title(f'TSP最优路径 (n={n}, 总路程={obj_val:.2f})', fontsize=12, pad=15)
    ax1.set_xlabel('X', fontsize=10)
    ax1.set_ylabel('Y', fontsize=10)
    ax1.grid(True, alpha=0.3)

    # 右图：信息面板
    ax2.axis('off')
    info_text = f"""问题信息：
    • 节点数量：{n}
    • 总路程：{obj_val:.2f}
    • 求解时间：{time_total:.2f}秒
    • 近邻参数k：{k}
    • 算法：KDTree+DFJ

    路径信息：
    • 路径长度：{len(route) - 1}条边
    • 起点：节点{route[0]}
    • 终点：节点{route[-2]}
    • 是否闭环：是

    求解状态：
    • 方法：向量化KDTree
    • 状态：求解成功"""

    ax2.text(0.05, 0.5, info_text, fontsize=11, verticalalignment='center',
             bbox=dict(boxstyle="round,pad=0.5", facecolor="lightblue", alpha=0.5))
    plt.tight_layout()
    plt.savefig(f'result/tsp_route{n}_optimized.png', dpi=600, bbox_inches='tight')
    plt.show()
    plt.close('all')


def validate_solution(coords, route, obj_val, dist_matrix):
    """向量化验证"""
    if not route or len(route) < 2:
        return False

    n = len(coords)

    # 检查路径长度
    if len(route) != n + 1:
        print(f"路径长度错误：期望{n + 1}，实际{len(route)}")
        return False

    # 检查是否访问所有节点
    visited = set(route[:-1])
    if len(visited) != n:
        print(f"未访问所有节点：期望{n}，实际{len(visited)}")
        return False

    # 向量化计算总距离
    route_indices = np.array(route) - 1
    i_indices = route_indices[:-1]
    j_indices = route_indices[1:]

    # 使用高级索引快速获取距离
    calculated_dist = np.sum(dist_matrix[i_indices, j_indices]) + 1

    # 比较距离
    if abs(calculated_dist - obj_val) > 0.5:
        print(f"距离不匹配：求解器={obj_val:.4f}，计算={calculated_dist:.4f}")
        return False

    print(f"验证通过！求解器={obj_val:.4f}，计算距离={calculated_dist:.4f}")
    return True


# 主程序
if __name__ == "__main__":
    test_files = [
        "data/ch100.tsp"
    ]

    for filename in test_files:
        print(f"求解问题: {filename}")
        try:
            solver = TSPSolver(filename)
            model, obj_val, route, active_edges, time_total = solver.solve_tsp()

            if route and obj_val and len(route) == solver.n + 1:
                co_dict = {}
                for i in range(solver.n):
                    node_id = i + 1
                    co_dict[node_id] = (solver.coords[i][0], solver.coords[i][1])
                # 验证解
                if validate_solution(solver.coords, route, obj_val, solver.dist_matrix):
                    # 绘图
                    plot_tsp_route(
                        co_dict=co_dict,
                        route=route,
                        obj_val=obj_val,
                        time_total=time_total,
                        k=solver.k
                    )
                else:
                    print("警告：解验证失败")
            else:
                print("未找到有效路径（路径长度或格式错误）")

        except Exception as e:
            print(f"程序执行出错: {str(e)}")
            import traceback
            traceback.print_exc()
