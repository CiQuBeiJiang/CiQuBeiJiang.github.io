# Git 常用命令速查清单 (Cheat Sheet)

**简介**：Git 是目前最流行的分布式版本控制系统。这份清单涵盖了从项目初始化到远程协作的高频命令，按「开发工作流」逻辑分类，方便快速查阅。

---

## 1. 初始配置 (Config)

安装 Git 后首先要完成的基础配置，用于标识提交者身份，全局配置一次即可生效。

```Bash
# 设置用户名（与远程仓库账号关联，如 GitHub 用户名）
git config --global user.name "你的名字"

# 设置邮箱（与远程仓库绑定的邮箱）
git config --global user.email "你的邮箱@example.com"

# 查看当前所有配置信息（验证配置是否生效）
git config --list
```

---

## 2. 开始项目 (Start)

两种常见的项目启动方式：本地新建仓库，或从远程克隆已有仓库。

### 2.1 本地新建仓库

在当前文件夹初始化 Git 仓库，将普通文件夹转为 Git 可管理的项目目录。

```Bash
git init
```

### 2.2 克隆远程仓库

从 GitHub、GitLab、Gitee 等平台下载远程代码到本地，自动创建与远程仓库对应的本地目录。

```Bash
git clone 地址>
# 示例：git clone https://github.com/username/project-name.git
```

---

## 3. 日常工作流 (Workflow)

核心操作流程：**工作区 (Workspace) → 暂存区 (Index) → 本地仓库 (Repository)**，是日常开发中最高频的「三板斧」。

### 3.1 查看文件状态

随时检查工作区与暂存区的文件变动，明确哪些文件被修改、新增或待提交，是 Git 操作的「导航仪」。

```Bash
git status
```

### 3.2 添加到暂存区

将工作区的修改（新增、修改的文件）添加到暂存区，暂存区相当于「提交前的临时缓冲区」，可灵活选择要提交的文件。

```Bash
git add  # 添加单个/多个指定文件（空格分隔多个文件名）
git add .                # 添加当前目录下所有变化（包括新增、修改，不包含删除）
git add -A               # 添加所有变化（包括新增、修改、删除，推荐）
```

### 3.3 提交到本地仓库

将暂存区的文件永久保存到本地仓库，生成一条提交记录（包含提交说明、作者、时间等信息），是版本控制的核心步骤。

```Bash
git commit -m "提交说明"  # 提交说明需清晰，说明本次修改的内容（如功能开发、bug修复）
# 示例：git commit -m "Feat: 新增用户登录表单验证功能"
# 示例：git commit -m "Fix: 修复移动端适配时按钮错位问题"
```

**Tip**：提交说明建议遵循「类型: 描述」的格式，常见类型有 `Feat`（新功能）、`Fix`（bug修复）、`Doc`（文档修改）、`Style`（代码格式调整，不影响逻辑）等，便于后续查看历史记录时快速理解修改意图。

---

## 4. 分支管理 (Branch)

分支是 Git 的核心功能之一，用于隔离不同的开发任务（如功能开发、bug修复），避免代码相互干扰。**禁止直接在 master/main 分支开发**，应在子分支开发完成后合并到主分支。

### 4.1 查看与创建分支

```Bash
# 查看本地所有分支 (*表示当前所在分支)
git branch

# 创建新分支
git branch <分支名>

# 切换分支
git checkout <分支名>
# 或者用新命令 (更推荐)
git switch <分支名>

# 🔥 创建并立即切换到新分支 (最常用)
git checkout -b <分支名>
```

### 4.2 合并与删除分支

分支开发完成后，需合并到目标分支（如主分支 master/main），合并完成后可删除无用的子分支。

```Bash
# 合并分支步骤：先切换到目标分支，再合并源分支
# 示例：将 dev-login 分支合并到 master 分支
git switch master          # 1. 切换到 master 分支
git merge dev-login        # 2. 合并 dev-login 分支到当前分支（master）

# 删除本地分支（仅当分支已合并到目标分支时允许删除，避免误删未提交代码）
git branch -d  示例：git branch -d dev-login （合并完成后删除开发分支）

# 强制删除本地分支（适用于分支未合并但确认无用的场景，慎用！）
git branch -D <分支名>
```

---

## 5. 远程同步 (Remote)

与远程仓库（如 GitHub、GitLab）交互，实现代码的拉取（同步远程更新）与推送（上传本地代码），支持多人协作。

```Bash
# 查看当前项目关联的远程仓库地址（origin 是远程仓库的默认别名）
git remote -v

# 拉取远程分支的最新代码到本地（同步远程更新，避免冲突）
# Pull = Fetch（获取远程代码） + Merge（合并到本地分支）
git pull origin <分支名>
# 示例：git pull origin master （拉取远程 master 分支的最新代码）

# 推送本地分支到远程仓库（上传本地修改）
git push origin <分支名>
# 示例：git push origin dev-login （推送本地 dev-login 分支到远程）

# 🔥 第一次推送新分支到远程（需建立本地分支与远程分支的追踪关系）
# 推送后后续可直接用 git push，无需指定 origin 和分支名
git push -u origin <本地分支名>
# 示例：git push -u origin dev-login
```

---

## 6. "后悔药"与撤销 (Undo)

开发中难免出现错误（如提交错文件、代码写错），以下命令可在不同场景下撤销操作，**操作前建议先执行 git status 确认当前状态，避免误操作**。

### 6.1 撤销工作区修改

将文件恢复到最后一次 `git commit` 或 `git add` 后的状态，丢弃工作区未暂存的修改（不可逆，需确认无需保留修改）。

```Bash
# 旧命令
git checkout -- 
# 新命令（Git 2.23+ 支持，更直观）
git restore >
# 示例：git restore src/main/java/Login.java （撤销 Login.java 的工作区修改）
```

### 6.2 撤销暂存区修改

将文件从暂存区拉回工作区，即撤销 `git add` 操作，文件回到修改后的状态（仅取消暂存，不丢弃修改）。

```Bash
# 旧命令
git reset HEAD 
# 新命令
git restore --staged <文件名>
# 示例：git restore --staged src/main/java/Login.java （取消 Login.java 的暂存状态）
```

### 6.3 修改最后一次提交

如果刚提交完就发现提交说明写错，或漏加了文件，可修改最后一次提交（无需新增一条提交记录）。

```Bash
# 先将漏加的文件添加到暂存区（若有漏加文件）
git add >
# 再修改最后一次提交的说明
git commit --amend -m "新的提交说明"
# 示例：git commit --amend -m "Fix: 修复登录页验证码过期问题（补充漏加的验证逻辑文件）"
```

---

## 7. 实用工具 (Utilities)

### 7.1 查看提交日志

查看历史提交记录，可按不同格式展示，帮助追溯代码修改历史。

```Bash
# 查看完整提交日志（包含作者、时间、提交ID、提交说明）
git log

# 🔥 简化日志格式（一行显示一条记录，包含提交ID前7位、提交说明，非常直观）
git log --oneline

# 图形化展示分支合并历史（显示分支流向，多人协作时必备）
git log --oneline --graph --all
```

### 7.2 暂存工作现场 (Stash)

当你在一个分支开发到一半（代码未完成，不想提交），突然需要切换到另一个分支修复紧急bug时，可将当前工作区的修改暂存起来，待bug修复完成后再恢复。

```Bash
# 1. 暂存当前工作区的修改（清理工作区，不影响未跟踪的新文件）
git stash
# 可选：添加暂存说明，便于后续区分不同暂存内容
git stash save "暂存登录功能开发到一半的代码"

# 2. 切换到bug修复分支，完成修复并提交
git switch bug-fix
# ... 修复bug的代码修改 ...
git add .
git commit -m "Fix: 紧急修复首页加载空白问题"

# 3. 回到原开发分支，恢复暂存的代码（恢复后自动删除暂存记录）
git switch dev-login
git stash pop

# 查看所有暂存记录（若有多个暂存）
git stash list
# 恢复指定的暂存记录（如恢复第1条暂存，索引从0开始）
git stash apply stash@{0}
# 删除指定的暂存记录（恢复后未自动删除时使用）
git stash drop stash@{0}
```

### 7.3 忽略文件 (.gitignore)

在项目根目录创建 `.gitignore` 文件，用于指定 Git 无需跟踪的文件/目录（如编译生成的文件、日志、配置文件等），避免这些文件被误提交到仓库。

#### 常见 `.gitignore` 配置示例（根据项目类型调整）

```Plain Text
# Java 项目示例
/node_modules        # 依赖包目录（前端项目也常用）
/target              # 编译生成的class文件目录
*.log                # 所有.log后缀的日志文件
.env                 # 环境配置文件（可能包含密码、密钥）
.idea/               # IDEA 编辑器的配置目录
.vscode/             # VS Code 编辑器的配置目录
*.iml                # IDEA 项目的模块配置文件

# Python 项目示例（额外添加）
__pycache__/         # 编译生成的缓存目录
*.pyc                # 编译生成的.pyc文件
venv/                # 虚拟环境目录
```

**Tip**：.gitignore 文件本身需要提交到仓库，以便团队其他成员使用相同的忽略规则。

---

## 总结：Git 极简流程图

![Git Simple Flow Chart](/images/Git_Simple_FlowChart.png)

---

## 💡 实用建议

1. **`git status`** ** 是你的好朋友**：无论何时，只要不确定当前状态（如哪些文件已修改、是否有未提交内容），执行 `git status` 即可清晰了解，避免盲目操作。

2. **别怕犯错，善用版本记录**：只要代码已通过 `git commit` 提交到本地仓库，即使后续修改出错，也能通过 `git log` 找到历史提交ID，再用 `git checkout <提交ID> <文件名>` 恢复旧版本代码（具体用法可进一步学习）。

3. **新手推荐图形化工具**：记不住命令时，可使用 VS Code 自带的 Git 面板（左侧边栏「源代码管理」），或专用工具如 SourceTree、GitKraken，图形化界面能直观展示分支、提交记录，降低操作门槛。

4. **多人协作先拉后推**：每次推送代码到远程前，先执行 `git pull` 拉取远程最新代码，避免因本地代码落后于远程导致合并冲突。