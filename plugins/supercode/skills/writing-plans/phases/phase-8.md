# 阶段 8：执行交接

**前提：阶段 7 已完成。**

## 目标

告知用户下一步操作。

## 执行方式

### 小型设计：直接执行

告知用户：

```
计划完成并保存到 `docs/plans/YYYY-MM-DD-<topic>-plan.md`。

你应该结束本次会话，开启新的会话，并复制以下命令到新的会话窗口：

/executing-plans docs/plans/YYYY-MM-DD-<topic>-plan.md
```

### 中/大型设计：分阶段执行

告知用户：

```
阶段性计划完成！

路线图：docs/plans/YYYY-MM-DD-<topic>-roadmap.md

**执行步骤：**

1. 结束本次会话，开启新的会话
2. 从阶段1开始执行：
   /executing-plans docs/plans/YYYY-MM-DD-<topic>-phase1-plan.md

3. 阶段1完成后，运行验收测试，确认通过后继续下一阶段
4. 执行阶段2：
   /executing-plans docs/plans/YYYY-MM-DD-<topic>-phase2-plan.md

5. 依次执行所有阶段

**重要提醒：**
- 每个阶段完成后必须运行验收测试
- 只有当前阶段通过验收后，才进入下一阶段
- 如果某个阶段验收失败，修复问题后重新运行验收测试
```

## 任务清单

```markdown
[
  {"content": "告知用户执行步骤", "status": "in_progress", "activeForm": "正在告知用户执行步骤"}
]
```

## 本阶段输出

- 用户已知晓下一步操作

## 完成条件

用户已确认知晓下一步，本次 skill 执行完成。
