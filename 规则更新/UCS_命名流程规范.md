# UCS 音效命名流程规范

> 版本：v1.4　制定日期：2026-08-20　状态：执行中

## 〇、路径与配置（跨设备部署）

- 本规范中所有 `<UCS_ROOT>` 为**根目录占位符**，不写死绝对路径；本机根目录为 `D:\Ai_Project\UCS`
- skill 会话第一步按探测协议定位根目录：环境变量 `UCS_ROOT` → 工作区自检（含三子目录）→ 常见位置扫描 → 询问用户
- 习惯差异通过 `ucs-config.default.json`（标准）+ `ucs-config.local.json`（本地覆盖）配置，**个性化工作，标准化提交**
- 跨设备部署与配置细则见《Skill跨设备部署与用户习惯适配方案.md》与 skill 内 `install.md`

## 一、流程总览

```
扫描音效库目录 → 附带文件处理 → UCS 命名与中文翻译 → 生成双列 .txt 映射清单
→ 矛盾检查 → 批量重命名（dry-run → 执行 → 校验）→ 工作日志归档
```

---

## 二、输入：附带文件处理

### 音频文件白名单
仅以下扩展名参与命名与重命名：

```
.wav　.mp3　.flac　.aif　.ogg
```

### 库自带说明文件（删除）
- 音效库自带的说明/信息文件（`.txt　.pdf　.jpg　.png　.html　.htm　.md　README` 等）一律**删除**，不进入清单、不重命名。
- 删除前必须 dry-run 预览完整删除清单，经用户确认后才执行。
- 仅删除库发布时自带的文档；无法确认来源的文件先跳过并标注「待确认」。
- 删除记录写入工作日志（数量 + 清单）。

---

## 三、输出：双列 .txt 映射清单

### 格式选型结论
**.txt 纯文本最稳定**：无格式解析歧义，脚本可逐行精确解析；.md 表格依赖分隔符，文件名含特殊字符会破坏表格。故采用 .txt 双列。

### 文件命名
清单文件名须保留修改者（Agent）信息，格式：
```
UCS_命名清单_<修改Agent>_<库名>.txt
```
示例：`UCS_命名清单_WorkBuddy_BOOM_Canyons.txt`
- `<修改Agent>` 即执行命名/翻译的 Agent 名称，与头部「翻译Agent」字段一致
- 同一库被不同 Agent 修改时，各自保留独立清单文件，不做覆盖合并

### 头部元信息（含翻译 Agent）
```
UCS 音效命名清单
音效库：<库名>
文件总数：N
生成日期：YYYY-MM-DD
翻译Agent：<Agent名称>（模型：Auto）
CreatorID：<如有> | SourceID：<如有>
说明：第一列=原文件名，第二列=翻译后文件名，TAB 分隔；本文件即批量重命名脚本的唯一输入。
```

### 数据行
```
原文件名<TAB>翻译后文件名
QP12 1425 Canyons dawn stillness.wav<TAB>【（环境_鸟鸣）黎明，静谧】AMBBird_QP12 1425 Canyons dawn stillness.wav
```

### 补建范围
Canyons / Debris / Magic_Alchemy / Futuristic_Interface 四个已完成库，从现有清单还原原文件名，覆盖更新为双列格式。

---

## 四、文件夹中文翻译规则

另见独立文档 `文件夹翻译规则.md`（本次仅定规则，不执行）。

统一格式：`【中文翻译】英文原名`，示例：`Risers` → `【上升】Risers`。

---

## 五、矛盾检查（每次更新必做）

- [ ] CatID 全部来自 `ucs-zh-en.tsv` 对照表，不猜测、不创造
- [ ] 中文分类遵循 `known-conflicts.md` 裁决（AMBNaut、OBJ 错位、GUN/BOAT 统一）
- [ ] 格式：无空行、【】紧贴英文文件名、中文逗号分隔、关键词 2-5 个
- [ ] 无重名；无残留英文关键词
- [ ] 新规则与既有规则对照，矛盾写入 `known-conflicts.md`

### 规则文件双轨管理（v1.4 起）
- **编辑源**（改规则在此，安全可审阅）：`<UCS_ROOT>\规则更新\known-conflicts.md`（本机：`D:\Ai_Project\UCS\规则更新\known-conflicts.md`）
- **发布副本**（skill 运行时读取）：skill `references\known-conflicts.md`
- 流程：**项目改 → 审阅 → 同步 skill references →（按需）打包 zip**
- 目的：避免直接改 skill 改坏；规则变更留日志可追溯；skill 保持自包含可传播
- 同理适用于 skill 内其他规则文件（`naming-rules.md`、`ucs-filenaming-guide.md`），需要时复制同名工作版入 `<UCS_ROOT>\规则更新\`

---

## 六、批量重命名流程

1. 以双列清单为唯一输入
2. dry-run：原文件名 100% 匹配、目标零冲突
3. 执行：原位重命名
4. 校验：重命名后数量与清单一致
5. 写工作日志

---

## 七、工作日志（每次执行必写）

- 每次命名/重命名执行后，追加到 `<UCS_ROOT>\日志\<Agent>_YYYY-MM-DD.md`（本机：`D:\Ai_Project\UCS\日志\`）
- 多 Agent 各自写独立日志文件（文件名带 Agent 前缀），避免同日互相覆盖
- 日志模板：库名 / 文件总数 / CatID 分布 / 附带文件处理（删除数）/ 源路径 / dry-run 与执行结果 / 规则要点
- 长期约定写入 `D:\Ai_Project\UCS\日志\MEMORY.md`
- 多 Agent 协作细则另见《多Agent协作_Skill文件输出管理方案.md》

---

## 八、项目结构与执行记录

### 项目目录（根目录即 `<UCS_ROOT>`，本机为 D:\Ai_Project\UCS；目录名可按 `ucs-config.local.json` 自定义）
```
<UCS_ROOT>\
├── 日志\         # 工作日志（<Agent>_YYYY-MM-DD.md）与长期记忆 MEMORY.md
├── 命名清单\     # 双列 .txt 映射清单（UCS_命名清单_<Agent>_<库名>.txt）
└── 规则更新\     # 本规范 / 文件夹翻译规则.md / 多Agent协作方案 / 跨设备方案
```

### 执行记录
1. v1.0：产出本规范与 `文件夹翻译规则.md`（已完成）
2. 4 库清单覆盖更新为双列格式（已完成，2026-08-20）
3. 清单文件重命名加入 Agent 标识，项目文件迁移至 D:\Ai_Project\UCS（已完成）
4. 同步更新 `ucs-sound-naming` skill（master→副本→zip，已完成，2026-08-20）
5. v1.2：日志命名改为 `<Agent>_YYYY-MM-DD.md`，产出《多Agent协作_Skill文件输出管理方案.md》（已完成）
6. 豆包 5 清单转双列并纳入统一管理（已完成，2026-08-20）
7. v1.3：产出《Skill跨设备部署与用户习惯适配方案.md》，skill 路径零假设改造（`<UCS_ROOT>` + 探测协议 + ucs-config + install.md），zip 重打包发布（已完成）
8. v1.4：规则文件双轨管理（known-conflicts 工作版入规则更新）；zip 改为按需打包；字符上限不设限（保留官方 FXName≤25 建议）（本次完成）
