# 多 Agent 协作：Skill 文件输出管理方案

> 版本：v1.0　制定日期：2026-08-20　状态：执行中
> 适用对象：所有使用 `ucs-sound-naming` skill 的 AI Agent（WorkBuddy、豆包、DeepSeek 等）

---

## 一、背景与问题

`ucs-sound-naming` skill 正在向多个 AI Agent 平台传播（WorkBuddy / 豆包 / DeepSeek 等）。多 Agent 共同产出时，若无统一管理会出现：

- **清单格式不统一**：豆包产出单行式（`【中文】英文`），WorkBuddy 产出双列映射，混在一起无法直接喂给重命名脚本
- **归属不可追溯**：文件里没有「谁翻译、何时翻译」信息，出错无法定位责任 Agent
- **日志互相覆盖**：多 Agent 同一天写 `2026-08-20.md` 会互相覆盖
- **规则版本漂移**：各平台手里的 SKILL.md / references 版本不一致，输出口径逐渐分叉

**本方案目标**：统一所有 Agent 的**文件输出规范**，保证多 Agent 共用一个 skill 时——格式一致、归属可查、日志不冲突、规则版本单一。

---

## 二、核心原则

1. **单一事实来源（Single Source of Truth）**：命名规则、矛盾裁决、对照表只以一处为准，其他都是副本
2. **文件必须可追溯**：谁翻译（Agent）、何时翻译（日期）、依据哪个规则版本，文件内可查
3. **格式机器可读**：一切面向重命名脚本的文件用 .txt 双列，不用 .md 表格
4. **Agent 标识进文件名**：清单、日志文件名均带 Agent 名，物理隔离同名冲突

---

## 三、统一文件命名规范（全部 Agent 强制）

### 3.1 命名清单
```
UCS_命名清单_<Agent>_<库名>.txt
```
示例：`UCS_命名清单_WorkBuddy_BOOM_Canyons.txt`、`UCS_命名清单_豆包_大草原音效.txt`

### 3.2 工作日志
```
<Agent>_YYYY-MM-DD.md
```
示例：`WorkBuddy_2026-08-20.md`、`豆包_2026-08-20.md`

> 多 Agent 同一天各自写日志，文件名不同，互不覆盖。

### 3.3 规则文档
```
<文档名>_v<X>.<Y>.md
```
示例：`UCS_命名流程规范_v1.1.md`（历史版本不删除，按版本保留）

---

## 四、统一目录结构

所有 Agent 的**最终产出**统一汇入 `D:\Ai_Project\UCS\`：

```
D:\Ai_Project\UCS\
├── 日志\            # 所有 Agent 的工作日志（<Agent>_YYYY-MM-DD.md）
├── 命名清单\        # 所有 Agent 的双列清单（UCS_命名清单_<Agent>_<库名>.txt）
└── 规则更新\        # 规则文档（含版本号）+ 本方案 + skill 更新记录
```

### 4.1 清单头部信息（每份必含）
```
UCS 音效命名清单
音效库：<库名>
文件总数：N
生成日期：YYYY-MM-DD
翻译Agent：<Agent名称>（模型：Auto）
CreatorID：<如有> | SourceID：<如有>
说明：第一列=原文件名，第二列=翻译后文件名，TAB 分隔；本文件即批量重命名脚本的唯一输入。
```

### 4.2 各 Agent 本地工作目录
Agent 可在本地目录（如 `D:\Ai_Project\DouBao\`）自由工作，但**完成后必须将清单提交到 `命名清单\`、将日志提交到 `日志\`**，本地仅作草稿区。

---

## 五、多 Agent 协作规则

1. **同一库同一时间只由一个 Agent 维护**：命名清单头部「翻译Agent」即该库负责人；其他 Agent 若需更新，先读取现有清单，确认负责人并与其日志核对后再改。
2. **更新不覆盖、产新版**：已有清单的库再次命名时，新增内容合并重生成，或另产新文件，不静默覆盖历史。
3. **重命名执行前必须 dry-run**：以最新清单为唯一输入，原文件名 100% 匹配、目标零冲突，才允许执行。
4. **修改必有日志**：任何 Agent 在 `日志\` 追加一条 `<Agent>_YYYY-MM-DD.md`，说明改了什么库、多少条、依据规则版本。
5. **规则有矛盾先裁决**：遇到分类歧义，先查 `known-conflicts.md`；新增裁决写入该文件，不得各 Agent 各按各的理解输出。

---

## 六、Skill 版本与分发管理

### 6.1 版本拓扑
```
master（唯一事实来源）
  C:\Users\Administrator\.workbuddy\skills\ucs-sound-naming

分发副本（供平台使用）
  D:\Ai_Project\Skills\ucs-sound-naming\

发布包（分发用）
  D:\Ai_Project\Skills\ucs-sound-naming.zip
```

### 6.2 同步流程（skill 修改后执行）
1. 修改 master（用户级 skill）
2. 同步到分发副本 `D:\Ai_Project\Skills\ucs-sound-naming\`（覆盖 SKILL.md、references、脚本）
3. 打包 zip 为**按需执行**：仅在需要发布/传播时重打包；日常小改跳过
4. `UCS_命名流程规范.md` 版本号 +1（小改 +0.1，大改 +1）
5. 在当日日志记录本次修改

### 6.3 规则文档发布口径
- `ucs-zh-en.tsv` 对照表与 `known-conflicts.md` 是**规则权威**，任何 Agent 不得自行增删 CatID 或改变裁决
- 分发副本/zip 若与 master 不一致，以 master 为准，副本视为过期

---

## 七、落地清单

| # | 事项 | 状态 |
|---|---|---|
| 1 | 产出本方案文档 | 本次完成 |
| 2 | master → 分发副本 → zip 全量同步 | 本次执行 |
| 3 | 既有日志补 Agent 前缀（WorkBuddy_2026-08-19/20.md） | 本次执行 |
| 4 | 建立 MEMORY.md 长期约定 | 本次执行 |
| 5 | 豆包 5 个清单（412 条）转双列格式 + Agent 标识 | 本次执行（2026-08-20） |
| 6 | 规范文档升级 v1.2（纳入日志命名新规则） | 本次执行 |
| 7 | 产出《Skill跨设备部署与用户习惯适配方案.md》（路径探测 + 配置化） | 本次执行 |

---

## 八、各 Agent 接入流程（给新 Agent）

1. 获取最新 skill：`D:\Ai_Project\Skills\ucs-sound-naming\`（或解压 zip）
2. 阅读 `README-介绍.md` 了解能力；阅读 `references/naming-rules.md` 与 `known-conflicts.md` 了解规则
3. 命名产出按本文档第三节命名、第四节归档
4. 完成后写日志到 `D:\Ai_Project\UCS\日志\<Agent>_YYYY-MM-DD.md`
5. 不确定的分类先提问或查表，不猜测
