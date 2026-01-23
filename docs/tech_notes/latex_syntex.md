# LaTeX 极简入门与语法速查手册

**简介**：LaTeX (读作 "Lay-tech" 或 "Lah-tech") 是一种基于 TeX 的排版系统。它不讲究“所见即所得”，而是“所想即所得”。你专注于内容和逻辑，格式交给编译器。

---

## 1. 工具推荐 (新手必读) 

**新手强烈建议从「在线编辑器」开始，无需安装几十 GB 的环境，打开网页就能用。**

### 方案一：在线编辑器 (最推荐)

- **Overleaf** (`overleaf.com`)

    - **优点**：无需配置，打开浏览器就能写；支持实时预览；有海量模板（论文、简历、作业）。

    - **建议**：注册一个账号，新建一个 "Blank Project"，把下面的代码复制进去试运行。

### 方案二：本地安装 (进阶)

如果你想在断网时使用，或者追求极致响应速度：

1. **安装编译器 (引擎)**：

    - Windows: **TeX Live**

    - macOS: **MacTeX**

2. **安装编辑器 (界面)**：

    - **VS Code** + **LaTeX Workshop 插件** (最现代化，推荐程序员使用)。

    - **TeXStudio** (经典老牌，功能全但界面较旧)。

---

## 2. LaTeX 文档结构 (骨架)

一个标准的 `.tex` 文件由**导言区 (Preamble)** 和 **正文区 (Body)** 组成。

```LaTeX
% --- 导言区 (配置全局设置) ---
\documentclass[12pt]{article}  % 文档类型：article(文章), book(书), beamer(PPT)

% 引入宏包 (相当于 Python 的 import / Java 的 library)
\usepackage[utf8]{inputenc}    % 编码支持
\usepackage{amsmath}           % 数学公式增强包 (必选)
\usepackage{graphicx}          % 插入图片包
\usepackage{geometry}          % 页面边距设置
\usepackage{ctex}              % 中文支持 (写中文必须加这个！)

% 页面设置
\geometry{a4paper, scale=0.8} 

% --- 正文区 (内容在这里) ---
\begin{document}

    \title{我的第一个 LaTeX 文档}
    \author{你的名字}
    \date{\today}
    
    \maketitle  % 生成标题页
    
    \section{引言}
    这里是正文的第一段。LaTeX 会自动处理首行缩进。
    
    \subsection{背景}
    这是二级标题。

\end{document}
```

## 3. 基础语法速查

### 文本样式

| 效果     | 语法             | 备注                    |
| -------- | ---------------- | ----------------------- |
| 加粗     | \textbf{内容}    | Bold                    |
| 斜体     | \textit{内容}    | Italic                  |
| 下划线   | \underline{内容} | -                       |
| 等宽字体 | \texttt{内容}    | 类似代码样式            |
| 换行     | \\ 或 空一行     | 空一行表示换段落 (推荐) |
| 换页     | \newpage         | 强制换到下一页          |

### 特殊字符转义

LaTeX 中有些符号有特殊含义，如果要显示它们本身，需要加 `\`：

- % (注释符) → %

- $ (数学符) → \$ 

- _ (下标符) → _

- & (对齐符) → &

- {} (分组符) → { }

- \ (转义符本身) → \textbackslash

## 4. 数学公式 (核心功能)

LaTeX 的数学排版是世界最强的。需要引入 `\usepackage{amsmath}`。

### 插入模式

- 行内公式 (混在文字里)：使用 `$ ... $`

例：Einstein said  $E=mc^2$ .

- 行间公式 (独占一行居中)：使用 `[ ... ]` 或 `\begin{equation} ... \end{equation}` (带编号)。

例：

```LaTeX
\[
  F = G \frac{m_1 m_2}{r^2}
\]
```

### 常用数学符号 (Cheat Sheet)

| 描述     | LaTeX 代码                 | 渲染预览                     |
| -------- | -------------------------- | ---------------------------- |
| 分数     | \frac{a}{b}                | $\frac{a}{b}$                |
| 上/下标  | x^2, a_{ij}                | $x^2, a_{ij}$                |
| 根号     | \sqrt{x}, \sqrt[3]{y}      | $\sqrt{x}, \sqrt[3]{y}$      |
| 求和     | \sum_{i=1}^{n} i           | $\sum_{i=1}^{n} i$           |
| 积分     | \int_{0}^{\infty} x dx     | $\int_{0}^{\infty} x dx$     |
| 希腊字母 | \alpha, \beta, \lambda     | $\alpha, \beta, \lambda$     |
| 大号括号 | \left( \frac{a}{b} \right) | $\left( \frac{a}{b} \right)$ |

### 多行公式对齐

使用 align 环境，用 `&` 指定对齐位置，用 `\\` 换行。

```LaTeX
\begin{align}
    a &= b + c \\
      &= d + e
\end{align}
```

(效果：等号会对齐)

## 5. 列表与枚举

### 无序列表 (Bullet points)

```LaTeX
\begin{itemize}
    \item 苹果
    \item 香蕉
\end{itemize}
```

### 有序列表 (Numbered list)

```LaTeX
\begin{enumerate}
    \item 第一步
    \item 第二步
\end{enumerate}
```

## 6. 插入图片与表格

### 插入图片

需在导言区加 `\usepackage{graphicx}`。

```LaTeX
\begin{figure}[h]  % h 表示 here (尽量放在当前位置)
    \centering     % 图片居中
    \includegraphics[width=0.8\textwidth]{image.jpg} % 宽度设为页面宽度的80%
    \caption{这是图片的标题}
    \label{fig:my_image} % 用于文中引用
\end{figure}
```

### 简单表格

使用 tabular 环境。{c|c|c} 表示三列居中，中间有竖线。

```LaTeX
\begin{table}[h]
    \centering
    \begin{tabular}{|c|c|c|}
        \hline
        姓名 & 年龄 & 成绩 \\
        \hline
        张三 & 18 & 90 \\
        李四 & 19 & 85 \\
        \hline
    \end{tabular}
    \caption{学生成绩表}
\end{table}
```

## 7. 避坑指南 (易错点) 

### 中文乱码

- 一定要在导言区加上 `\usepackage{ctex}`。

- 编译器（Compiler）建议选择 XeLaTeX (Overleaf 的 Menu -> Compiler 中设置)，它对中文支持最好。

### 引号的方向

- 不要直接用键盘上的双引号 "。

- 左引号是 tab键上面那个键 (`)，右引号是单引号键 (')。

- LaTeX 写法：``引用内容'' (两个后也就是左引号，两个单引号)。

### 报错不要慌

- LaTeX 报错通常很难懂。最常见的错误是花括号不匹配 `{}` 或者忘记结束环境 (写了 begin 没写 end)。

---

### 你的第一步行动

1. 打开 [Overleaf.com](https://www.overleaf.com/) 注册账号。

2. 点击 "New Project" -> "Blank Project"。

3. 把上面 **「2. LaTeX 文档结构」** 中的代码复制进去。

4. 点击绿色的 **"Recompile"** 按钮。

5. 如果你看到生成的 PDF 里有中文标题，恭喜你，你已经入门了！

### 总结

1. LaTeX 入门优先选择 Overleaf 在线编辑器，无需配置环境，新手友好；本地使用需安装编译器+编辑器组合。

2. LaTeX 文档核心分为导言区（配置）和正文区（内容），写中文必须引入 `ctex` 宏包并使用 XeLaTeX 编译。

3. 数学公式是 LaTeX 核心优势，行内公式用 `$...$`，行间公式用 `[...]`，常用符号需熟记基础语法。