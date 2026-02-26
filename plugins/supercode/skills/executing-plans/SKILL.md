---
name: executing-plans
description: 在独立会话中执行已编写的实施计划时使用，并在检查点进行审查
---

# 执行计划（Executing Plans）

## 概述

加载计划，批判性审查，批量执行任务，在批次之间汇报审查。

**核心原则：** 带有架构师审查检查点的批量执行。

**开始时声明：** "我正在使用 executing-plans skill 来实施这个计划。"

## 流程

### 步骤 1：加载和审查计划
1. 读取计划文件
2. 批判性审查 - 识别计划中的任何问题或疑虑
3. 如果有疑虑：在开始前与人类合作伙伴提出
4. 如果没有疑虑：创建 TodoWrite 并继续

### 步骤 2：执行批次
**默认：前 3 个任务**

对于每个任务：
1. 标记为 in_progress
2. 严格遵循每个步骤（计划包含小步骤）
3. 按指定运行验证
4. 标记为 completed

### 步骤 3：汇报
当批次完成时：
- 展示已实现的内容
- 展示验证输出
- 说："准备接收反馈。"

### 步骤 4：继续
基于反馈：
- 如有需要应用更改
- 执行下一个批次
- 重复直到完成

### 步骤 5：验证测试并合并

所有任务完成并验证后：

**步骤 5.1：验证所有测试通过**

```bash
# 运行项目的测试套件
npm test / cargo test / pytest / go test ./...
```

**如果测试失败：**
- 停止执行
- 报告测试失败情况
- 等待用户修复指示

**如果测试通过：** 继续到步骤 5.2

**步骤 5.2：确定基础分支**

```bash
# 获取当前feature分支从哪个分支分出
git show-branch | sed 's/].*//' | grep '*' | grep -v "$(git rev-parse --abbrev-ref HEAD)" | head -1 | sed 's/.*\[//'

# 或者使用更可靠的方法
git merge-base HEAD main 2>/dev/null && echo "main" || git merge-base HEAD master 2>/dev/null && echo "master"
```

确认基础分支名称。

**步骤 5.3：合并到基础分支**

```bash
# 切换到基础分支
git checkout <base-branch>

# 拉取最新内容（如果有远程）
git pull origin <base-branch>

# 合并feature分支
git merge <feature-branch>

# 在合并结果上验证测试
npm test / cargo test / pytest / go test ./...
```

**如果合并后测试失败：**
- 报告冲突或失败情况
- 等待用户处理

**如果合并后测试通过：**

**步骤 5.4：清理分支**

```bash
# 删除已合并的feature分支
git branch -d <feature-branch>
```

**完成报告：**
"已完成实现，测试通过，已合并到 <base-branch>，分支已清理。"

## 何时停止并寻求帮助

**立即停止执行当：**
- 批次中途遇到阻碍（缺少依赖、测试失败、指令不清楚）
- 计划存在严重缺口导致无法开始
- 你不理解某个指令
- 验证反复失败

**要求澄清而不是猜测。**

## 何时重新审视之前的步骤

**返回到审查（步骤 1）当：**
- 合作伙伴根据你的反馈更新了计划
- 基本方法需要重新思考

**不要强行突破阻碍** - 停下来询问。

## 记住
- 首先批判性审查计划
- 严格遵循计划步骤
- 不要跳过验证
- 当计划提到时参考 skills
- 批次之间：只需汇报并等待
- 遇到阻碍时停止，不要猜测
- 没有明确的用户同意，永远不要在 main/master 分支上开始实现

## 集成

**必需的工作流程技能：**
- **superpowers:writing-plans** - 创建此技能执行的计划
- **superpowers:code-quality-review** - 实现完成后的代码质量审查
- **superpowers:finishing-a-development-branch** - 合并到基础分支

**工作流程：**
1. **brainstorming** - 创建 feature 分支
2. **writing-plans** - 编写实施计划
3. **executing-plans** - 执行计划
4. **code-quality-review** - 代码质量审查（推荐）
5. **finishing-a-development-branch** - 合并到基础分支
