---
name: ucs-sound-naming
description: 根据 UCS（Universal Category System）8.2.1 分类标准为音效文件生成规范命名清单，输出包含 CatID、英文关键词与中文翻译的完整文件名。当用户提供音效描述（中文或英文）、要求为音效命名或翻译音效文件名、提及 UCS 分类、CatID、音效命名时使用。
---

# UCS Sound Naming

为音效文件生成符合 UCS（Universal Category System）8.2.1 标准的命名清单。输入是音效描述，输出为「原文件名 → 翻译后文件名」的双列映射，按需生成可下载的 .txt 清单。

## 定位工作根目录（会话第一步，必做）

skill 内所有路径引用使用占位符 `<UCS_ROOT>`，**不写死绝对路径**。每次会话开始时按顺序探测根目录：

1. **环境变量 `UCS_ROOT`**（首选）：命中即用，零歧义
2. **当前工作区自检**：当前目录或其父目录是否直接含 `命名清单 / 日志 / 规则更新` 三个子目录
3. **常见位置扫描**：依次检查 `D:\Ai_Project\UCS`、`~/UCS`、`~/Documents/UCS`
4. **均未命中 → 询问用户**，并引导按 `install.md` 完成首次部署（建目录 + 配置环境变量）

确定根目录后：清单写入 `<UCS_ROOT>/命名清单/`，规则文档在 `<UCS_ROOT>/规则更新/`，日志追加到 `<UCS_ROOT>/日志/`。

## 工作流

1. **理解描述**：阅读用户提供的音效描述（中英文均可）。
2. **匹配 CatID**：从完整对照表 `references/ucs-zh-en.tsv` 中匹配最合适的 CatID。只使用 UCS 8.2.1 列表中存在的 CatID，不得猜测或创造。
3. **生成英文命名**：按 UCS 官方格式 `CatID_FXName_CreatorID_SourceID` 生成（块间用 `_` 分隔；FXName 为描述性命名词、**空格分隔单词**，原文件编号置于关键词后、调性前；CreatorID 取自库元数据；SourceID 有则追加、无则省略）。
4. **生成中文翻译**：在英文文件名前添加【（中文分类）中文关键词1，中文关键词2，...】（中文逗号分隔），紧贴英文部分、无空格。
5. **输出映射并确认归档**：先向用户展示双列映射（`原文件名<TAB>翻译后文件名`，保留格式后缀），随后**询问是否写入 .txt 清单文件**——默认生成，文件名 `UCS_命名清单_<修改Agent>_<库名>.txt`（示例 `UCS_命名清单_WorkBuddy_BOOM_Canyons.txt`）；按需可跳过（`ucs-config.local.json` 中 `listFile.enabled=false` 可默认关闭，关闭后映射仅留在会话中，需归档时随时可重新生成）。
6. **写工作日志**：执行后追加到 `<UCS_ROOT>/日志/<Agent>_YYYY-MM-DD.md`。

## 核心规则（要点）

- 仅基于 UCS 8.2.1 标准分类，CatID 必须来自对照表，大小写不可更改。
- **Foley 限制**：FOLY* 目录仅用于对画面表演的官方干净拟音；户外的、非正式的、自录的素材不要归入 Foley 目录，改用 FOOTSTEPS（FEET*）或 OBJECT（OBJ*）类。
- 描述模糊时：提供多个可能的 CatID 并说明各自适用理由；信息不足时先向用户提问。
- 已按 UCS 命名好的文件可直接进入翻译步骤：英文部分（含 CreatorID、SourceID）不更改。
- whoosh 翻译为"呼啸"；调式（如 F#m）也翻译进【】内的中文关键词中。
- 中文关键词 2-5 个（推荐值）；若英文为 UCS 官方命名，中英文关键词数量跟随英文。
- 文件名总长不设上限（官方 FXName≤25 仅约束 FXName 单块，不约束整条文件名）。
- 文件名中不要出现重复词语；重名时依次追加编号区分，新编号放源文件关键词最后，原有编号保留。
- 若原文件名开头有编号，该编号置于中文关键词序列末尾、调性之前；其他位置的编号仍保留原位。
- 输出应简洁、专业，术语准确、客观，面向音效设计师与媒体归档人员。

## 输出格式（双列 .txt 映射清单）

- **生成策略**：默认生成，输出前询问用户是否写入；`listFile.enabled=false` 可关闭，关闭后映射保留在会话中，随时可补生成
- 文件命名：`UCS_命名清单_<修改Agent>_<库名>.txt`，Agent 名与头部「翻译Agent」字段一致
- 头部元信息：库名 / 文件总数 / 生成日期 / 翻译Agent（名称+模型）/ CreatorID·SourceID / 说明（本文件即批量重命名脚本唯一输入）
- 数据行：`原文件名<TAB>翻译后文件名`，TAB 分隔
- 英文文件名格式：`CatID_FXName_CreatorID_SourceID`（FXName 空格分隔单词，原文件编号置于关键词后、调性前；CreatorID 取自库元数据；SourceID 有则追加、无则省略）
- 清单存放目录：`<UCS_ROOT>\命名清单\`
- 规则文档存放目录：`<UCS_ROOT>\规则更新\`
- 日志存放目录：`<UCS_ROOT>\日志\`

## 附带文件处理（输入扫描）

- 仅识别音频扩展名 `.wav .mp3 .flac .aif .ogg` 参与命名
- 库自带说明文件（`.txt .pdf .jpg .png .html .htm .md README` 等）一律**删除**，不入清单、不重命名；删除前 dry-run 预览经用户确认，无法确认来源的先标「待确认」

## 已知矛盾与修复记录

原始规则（见 `references/naming-rules.md`）中的示例与措辞矛盾已按 `references/known-conflicts.md` 的裁决修正；对照表仍有少量数据问题（见该文件 C 部分），遇到歧义时按其中标注处理。

## 资源

- `references/ucs-zh-en.tsv` — UCS 8.2.1 完整中英文对照表（753 行：Category / SubCategory / CatID / CatShort / Category_zh / SubCategory_zh / Synonyms_zh），按 CatShort 字母序排列，可直接查询任一 CatID 的中英文名称与同义词。
- `references/ucs-filenaming-guide.md` — UCS 官方文件名规范完整中文翻译（来自《UCS Filenaming Convention 2021》，含四信息块/三可选块/5 官方示例/结论）。
- `references/naming-rules.md` — 完整命名规则（15 条行为准则 + 基础版附录，示例与措辞已修正）。
- `references/known-conflicts.md` — 矛盾修复历史与数据问题清单（含裁决口径）。
