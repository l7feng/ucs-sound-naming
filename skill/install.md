# ucs-sound-naming 安装与部署引导

> 本文件随 skill 分发，指导新电脑首次部署。完成后即可让 AI Agent 开始音效命名工作。

---

## 部署四步

### 1. 建目录

在选定的根目录下创建三个子目录（目录名可按你的习惯修改，见第 3 步配置）：

```
<根目录>/
├── 命名清单\    # 双列 .txt 映射清单
├── 日志\        # <Agent>_YYYY-MM-DD.md 工作日志 + MEMORY.md
└── 规则更新\    # 规范文档、对照表、矛盾裁决
```

### 2. 配置环境变量 UCS_ROOT

把根目录写入系统环境变量，Agent 每次会话自动命中（探测协议第 1 级）：

```
Windows (cmd)    : setx UCS_ROOT "D:\Ai_Project\UCS"
Windows (PS)     : [Environment]::SetEnvironmentVariable("UCS_ROOT","D:\Ai_Project\UCS","User")
macOS / Linux    : echo 'export UCS_ROOT=~/UCS' >> ~/.zshrc   # 或 ~/.bashrc
```

> 设置后需重开终端/重启 AI 客户端才生效。也可以在 AI 会话中直接告知根目录路径，命中探测协议第 4 级（询问用户）。

### 3. 复制并调整本地配置

```
复制 ucs-config.default.json → 重命名为 ucs-config.local.json
```

`ucs-config.local.json` 是你的本地习惯配置，**不参与 skill 更新同步**，可修改项：

| 配置项 | 默认值（标准） | 说明 |
|---|---|---|
| `dirs` | 命名清单 / 日志 / 规则更新 | 目录名随你习惯改 |
| `listFile.template` | `UCS_命名清单_<Agent>_<库名>.txt` | 清单命名模板 |
| `logFile.template` | `<Agent>_YYYY-MM-DD.md` | 日志命名模板 |
| `naming.commaStyle` | fullwidth（中文逗号，） | 中文关键词分隔符 |
| `naming.keepCatidPrefix` | true | 是否保留英文名前的 CatID 前缀 |
| `folderTranslate.style` | `【中文翻译】英文原名` | 文件夹翻译风格 |
| `attachedFiles.action` | delete | 附带文件处理（删除/跳过/归档） |

> 红线不可改：`ucs-zh-en.tsv` 对照表、`known-conflicts.md` 矛盾裁决、UCS CatID 分类本体。

### 4. 自检

让 Agent 执行「定位工作根目录」，确认命中后再开始。自检通过标准：

- [ ] 能找到 `<UCS_ROOT>/命名清单/` 并读取已有清单
- [ ] `<UCS_ROOT>/日志/` 可写入，能看到历史日志
- [ ] `<UCS_ROOT>/规则更新/` 可读取本规范与矛盾裁决编辑稿（对照表为 skill 自带）

---

## 首次使用 Checklist

- [ ] 三目录已建好
- [ ] 环境变量 `UCS_ROOT` 已配置（或已告知 AI 根目录）
- [ ] `ucs-config.local.json` 已按习惯调整
- [ ] 对照表为 skill 自带（`references/ucs-zh-en.tsv`）；矛盾裁决编辑源在 `<UCS_ROOT>/规则更新/`，副本同步于 `references/known-conflicts.md`

## 常见问题

**Q：不想用环境变量可以吗？**
可以。把 AI 会话直接开在根目录（探测协议第 2 级），或每次告知路径（第 4 级）。环境变量只是最省事。

**Q：我改了目录名，Agent 找不到怎么办？**
在 `ucs-config.local.json` 的 `dirs` 中写明你的目录名；探测协议第 2 级会按配置的目录名自检。

**Q：skill 更新会不会覆盖我的本地配置？**
不会。skill 同步只覆盖 skill 目录内文件；`ucs-config.local.json` 放在你的根目录（建议放 `<UCS_ROOT>/规则更新/`），与 skill 目录分离。

**Q：和别人的清单/日志冲突怎么办？**
遵循多 Agent 协作方案：清单、日志文件名都带 Agent 标识（如 `UCS_命名清单_豆包_自然风声.txt`），物理隔离，互不覆盖。

---
