# 阶段 1：源码收集与目录初始化

前提：阶段 0 已完成。

## 目标

将所有源码本地化到 `source/` 目录。

## 执行方式

| 来源 | 处理方式 |
|------|----------|
| GitHub | `git clone --depth 1 {url} source/github/{repo-name}/` |
| npm 包 | 拉取源码（非打包产物）到 `source/npm/` |
| 网络 URL | 启动 Explore Task 交叉验证后保存到 `source/web/` |

网络信息规则：
- 禁止直接引用远程 URL 作为 source
- 必须交叉验证（至少两个独立来源一致）
- 验证后保存到 `source/web/`，内容包含：原始 URL、获取时间、验证来源

## 本阶段输出

完整的目录结构：

```
用户指定文件夹/
├── index.md              # 占位（阶段 3 填充）
└── source/               # 本阶段完成
    ├── github/
    ├── npm/
    └── web/
```

## 完成条件

所有源码已本地化，`source/` 目录结构完整，用户确认后进入阶段 2。
