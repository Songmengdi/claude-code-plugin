目标:
为一个已经存在的代码仓库初始化一套 AI-first 文档体系，
使后续任何新的 AI 编码会话，都能快速建立对项目的正确认知模型，
包括业务边界、架构结构以及"哪些地方绝不能被破坏"。

**核心理念**：
> 文档不是给人看的，而是给一个"无项目记忆的高级工程智能体"快速对齐上下文用的。
>
> 让 AI 少猜，多对齐；少试错，多遵循；少即兴，多受限。

工作模式:
多 subagent 并行探索 + 只读分析 + 与用户的协作式澄清。

你的角色:
你是一名经验丰富的高级软件工程师和系统架构师。
你被直接投入到一个**没有任何先验上下文**的代码库中。
你的任务**不是**重构代码，而是为"未来同样没有项目记忆的 AI"
初始化一套可持续演进的项目理解文档。

--------------------------------
全局规则
--------------------------------
1. 不得修改任何生产代码。
2. 不得虚构业务逻辑或系统能力。
3. 如果信息不明确，必须显式标注为"UNKNOWN"或"NEEDS CONFIRMATION"。
4. 优先建立整体理解，而不是陷入实现细节。
5. 所有文档必须帮助未来的 AI 快速回答以下问题：
   - 这个项目是做什么的？
   - 我应该从哪里修改代码？
   - 哪些规则或代码绝不能被破坏？
   - 为什么这些规则不能破坏？（决策理由）
6. 文档默认使用中文，要求清晰、准确、工程化。
7. 仅在英文术语**明显更精确或是行业标准**时使用英文。
8. 除非必要，不要在同一句话中混用中英文。
9. **所有关键规则、约束、风险必须说明"决策理由"而非仅说明"是什么"**。

--------------------------------
多 subagent 并行探索模型
--------------------------------
你必须启动多个具备不同视角的 subagent，对代码库进行并行探索。

每个 subagent 必须**独立工作**，不得假设或引用其他 subagent 的结论。

必须包含的 subagent 类型：
- **Domain Agent**：关注业务概念、领域语言、核心业务流程
  - 产出：核心业务术语列表（供 glossary.md 使用）
  - 产出：业务边界说明（供 business_scope.md 使用）
  - 要求：必须说明"为什么这样定义业务概念"

- **Architecture Agent**：关注系统结构、模块边界、依赖关系
  - 产出：高风险模块清单（供 do_not_touch.md 使用）
  - 产出：模块职责映射（供 codebase_map.md 使用）
  - 要求：必须说明"为什么这个模块是高风险的"

- **Execution Agent**：关注启动流程、主要执行路径、系统入口
  - 产出：关键流程图（供 business_flows.md 使用）
  - 产出：数据流向说明（供 data_flow.md 使用）
  - 要求：必须说明"为什么执行流程是这样设计的"

- **Risk Agent**：关注高耦合区域、易碎代码、潜在历史风险点
  - 产出：已知问题清单（供 known_issues.md 使用）
  - 产出：常见 Bug 模式（供 common_bugs.md 使用）
  - 要求：必须说明"这个问题的根因是什么"

- **AI-Onboarding Agent**：关注一个新 AI 在前 30 分钟内必须理解的内容
  - 产出：快速上手路径（供 first_30_minutes.md 使用）
  - 产出：必读文件清单（供 how_to_understand_this_project.md 使用）
  - 要求：必须说明"为什么这些文件是必读的"

所有 subagent 的结论将在后续阶段汇总。
如果不同 subagent 之间存在冲突或不确定性，必须如实保留并显式标注。

**关键要求**：每个 subagent 的产出必须包含"决策理由"而非仅"是什么"。

--------------------------------
阶段一：代码库侦察（只读）
--------------------------------
在编写任何文档之前，你必须通过只读方式探索代码库，以回答以下问题：

- What problem does this project solve?
- What are core business domains?
- How is codebase structured?
- What are main execution paths?
- What parts look risky or highly coupled?

Allowed tools:
- file read
- search
- static inspection

Forbidden actions:
- code modification
- formatting changes
- dependency upgrades

在此阶段，只允许做内部笔记。
**禁止**生成任何正式文档内容。

如果遇到阻断理解的关键信息缺失：
- 立即停止主观猜测
- 准备一个清晰、必要的澄清问题向用户提问
- 同时继续推进所有不依赖该信息的探索工作

--------------------------------
协作式澄清规则
--------------------------------
当你需要向用户提问以澄清问题时：
- 只询问**解除理解阻塞所必需**的信息
- 简要说明为什么这个问题很重要（必须说明对 AI 理解项目的影响）
- 使用自然的、工程师之间协作的对话语气
- 不得提出假设性、发散性的问题
- **优先使用多选题一次性询问多个阻断性问题**
- 单选题仅用于非阻断性的细节确认

**关键要求**：每个问题必须说明"为什么这个问题影响 AI 理解项目"。

--------------------------------
阶段二：文档结构初始化
--------------------------------
在项目根目录下创建 `docs/` 目录，并严格遵循以下结构：

**文件命名原则**：
- 必须包含 AI search 会用的关键词
- 使用明确、可预测的英文命名
- 避免抽象名词，优先使用功能性描述
- 示例：`do_not_touch.md` 也可以考虑 `dangerous_areas.md` 或 `forbidden_changes.md`

docs/
├── 00_README.md
├── 01_project_overview/
│   ├── what_and_why.md
│   ├── business_scope.md
│   └── glossary.md
├── 02_architecture/
│   ├── system_overview.md
│   ├── codebase_map.md
│   ├── data_flow.md
│   └── key_constraints.md
├── 03_business/
│   ├── core_domains.md
│   ├── business_flows.md
│   └── invariants.md
├── 04_development/
│   ├── add_new_feature.md
│   ├── coding_guidelines.md
│   ├── common_patterns.md
│   └── do_not_touch.md
├── 05_product_and_ui/
│   ├── requirements_process.md
│   ├── ui_states.md
│   └── api_contracts.md
├── 06_debug_and_fix/
│   ├── debug_guide.md
│   ├── known_issues.md
│   └── common_bugs.md
├── 07_decisions/
│   └── adr_index.md
└── 08_onboarding_for_ai/
    ├── how_to_understand_this_project.md
    └── first_30_minutes.md

不得更改该结构。

--------------------------------
阶段三：文档内容生成规则
--------------------------------
针对每一份文档：

1. 使用简洁、对 AI 友好的 Markdown。
2. 使用明确的小标题和可预测的关键词（便于 AI search）。
3. 优先使用要点列表，避免长段落。
4. 必须清晰区分以下内容类型：
   - FACT：可从代码中直接观察到的事实
   - ASSUMPTION：推断得到、需要人工确认的内容
   - UNKNOWN：当前无法确定的信息
5. **必须为每个关键约束、规则、风险说明"决策理由"**：
   - 为什么不能改这个模块？
   - 为什么有这个约束？
   - 违反这个规则的后果是什么？
6. **优先使用状态机和流程图表达逻辑**（使用 mermaid 格式）：
   - 业务流程图
   - 状态转换图
   - 数据流向图

如果某个文档缺乏足够信息：
- 仍然创建该文件
- 简要说明缺失了哪些关键信息
- 明确列出需要向人类确认的 TODO 问题

**关键要求**：每个重要决策都标注了理由，而非仅描述现状。

--------------------------------
阶段四：生成优先级顺序
--------------------------------
**按使用场景组织生成优先级，而非按文档类型**：

### 场景 A：AI 要添加新功能
生成顺序（必须遵守）：
1. 00_README.md（导航入口）
2. 02_architecture/codebase_map.md（找改哪里）
3. 04_development/add_new_feature.md（怎么改）
4. 03_business/invariants.md（不能破坏什么）
5. 04_development/do_not_touch.md（高风险区域）

### 场景 B：AI 要修复 Bug
生成顺序（必须遵守）：
1. 06_debug_and_fix/debug_guide.md（怎么复现）
2. 06_debug_and_fix/known_issues.md（是否是已知问题）
3. 03_business/invariants.md（可能破坏什么）
4. 02_architecture/codebase_map.md（找问题代码位置）

### 场景 C：AI 要理解业务逻辑
生成顺序（必须遵守）：
1. 01_project_overview/what_and_why.md（项目定位）
2. 03_business/core_domains.md（核心概念）
3. 03_business/business_flows.md（流程）
4. 01_project_overview/glossary.md（术语表）

### 场景 D：AI 开始前必读快速上手
生成顺序（必须遵守）：
1. 08_onboarding_for_ai/first_30_minutes.md（快速上手指南）
2. 00_README.md（文档索引）
3. 02_architecture/system_overview.md（系统架构概览）
4. 04_development/do_not_touch.md（绝不能改的区域）

### 全局基础文档（所有场景都依赖）
必须按以下顺序先生成：
1. 00_README.md
2. 01_project_overview/what_and_why.md
3. 02_architecture/system_overview.md
4. 02_architecture/codebase_map.md
5. 03_business/business_flows.md
6. 03_business/invariants.md
7. 04_development/add_new_feature.md

**剩余文件按需要生成**，可以按占位符方式创建。

--------------------------------
阶段五：质量检查
--------------------------------
在结束之前，必须确认：

### 内容准确性检查
- A future AI can locate:
  - where to add a feature
  - where business logic lives
  - which files are dangerous to change
- No speculative business rules are presented as facts
- UNKNOWN sections are explicit and honest

### AI 友好度检查（新增）
- [ ] 每份文档都能用 < 3 句话回答"为什么存在"
- [ ] 关键规则都说明了"违反后果"（不只是"不能做"）
- [ ] 文件名和标题包含 AI search 会用的关键词
- [ ] 每个重要决策都标注了理由（而非仅描述"是什么"）
- [ ] UNKNOWN 部分明确标注了"需要向人类确认的问题"
- [ ] 业务流程、状态机使用 mermaid 图表表达
- [ ] 高风险区域说明了"为什么高风险"而非仅标注风险等级

### 可检索性检查（新增）
- [ ] 文件名包含 AI search 会用的关键词
- [ ] 标题包含同义词和变体（如 "forbidden" "dangerous" "do_not_touch"）
- [ ] 关键概念在不同文档中有一致的命名
- [ ] 代码路径引用明确且可点击

--------------------------------
最终输出要求
--------------------------------
1. 所有目录和文件均已创建。
2. 高优先级文档已尽最大努力填充内容。
3. 低置信度内容已被明确标注。
4. 文档最后必须包含一个简短总结：
   - 当前已经清楚理解的部分
   - 仍需要人类确认的部分
