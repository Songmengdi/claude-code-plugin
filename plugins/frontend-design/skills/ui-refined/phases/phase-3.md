# 阶段 3：验证

## 目标

导出设计稿图片，优先让用户目视检查，必要时辅助自动化检查，发现问题则回到实现阶段修正。

## 步骤

### 3.1 导出图片

**始终使用 `scale: 1`**，低 scale 会导致图片模糊，影响分析准确性。

```bash
mcporter call pencil.export_nodes --args '{"nodeIds": ["frameId"], "format": "png", "scale": 1, "outputDir": "/tmp"}' > /tmp/export.json
```

### 3.2 用户目视检查（首选）

导出图片后，**优先让用户目视检查**。用户的视觉判断远快于自动化分析。

将导出的图片展示给用户，附上检查项清单：

- [ ] 无重复元素（同一区域出现相同内容）
- [ ] 无布局重叠（页面之间、组件之间）
- [ ] 对齐一致（同层级组件对齐方式统一）
- [ ] 文字无截断
- [ ] 间距一致（同类组件间距相同）
- [ ] 说明卡片与页面对应且内容完整

根据用户反馈直接修正问题，回到实现阶段。

### 3.3 自动化分析（补充）

仅在以下情况使用 analysis-images：

- 用户要求自动化检查
- 用户目视后仍有疑虑，需要辅助验证
- 页面数量多，用户希望批量初筛

```bash
mcporter call analysis-images.analysis_images --args '{"paths": ["/tmp/exported.png"], "prompts": ["检查是否有重复元素、布局重叠、对齐问题、文字截断、间距不一致等常见UI异常"]}' --timeout 120000
```

**不要完全信任分析结果。** analysis-images 可能漏报，关键问题应以用户判断为准。

### 3.4 深度检查（可选）

当目视检查不够时，用脚本深入检查节点结构。脚本位于 `scripts/` 目录，用法同实现阶段。

```bash
# 获取数据
mcporter call pencil.batch_get --args '{"ids": ["anyId"]}' --timeout 120000 > /tmp/pencil_output.json

# 查看节点树结构
python3 scripts/node_tree.py /tmp/pencil_output.json TARGET_ID

# 查看样式属性
python3 scripts/node_props.py /tmp/pencil_output.json ID1 ID2

# 提取 Design Token
python3 scripts/extract_tokens.py /tmp/pencil_output.json

# 对比组件变体
python3 scripts/diff_variants.py /tmp/pencil_output.json ID1 ID2 ID3
```

### 3.5 ⚠️ 不可避免的坑点

| 坑点 | 现象 | 处理方式 |
|------|------|----------|
| batch_get 大节点断连 | 查询包含大量子节点的 frame 时 MCP 连接关闭 | 不要一次查整棵树，改为先查子节点 ID 列表，再分批查询具体子节点 |
| analysis-images 可能漏报 | 图像分析报告"无异常"但实际存在问题 | 不要完全依赖分析结果，关键问题应以用户判断为准 |

## 完成条件

所有页面通过质量检查，或问题已修正并重新验证通过。
