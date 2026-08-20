# 通用分类系统（UCS）—— 文件命名规范

> 来源：*UCS Filenaming Convention 2021*  
> 发起者：Tim Nielsen 与 Justin Drury

---

## 1. 概述

UCS 大力推荐采用一种特殊的文件名结构。如果遵循该结构，各类程序中的自动化脚本便可以从文件名中自动解析信息，并填入最终用户的元数据字段。

该规范同时鼓励在文件名本身中提供最基本的信息——能够回答以下问题：

- 这个声音属于哪个类别和子类别？
- 这个声音是什么？
- 谁制作了这个声音？
- 它是为哪个项目或音效库制作的？

---

## 2. 基本文件名结构

UCS 基本文件名至少需要 **四个信息块**，每个块之间用下划线 `_` 分隔。下划线 **只能** 用于分隔这些块，不应在其他地方使用。

```
CatID_FXName_CreatorID_SourceID
```

| 信息块 | 定义 |
|--------|------|
| **CatID** | 缩写的类别 / 子类别（由 UCS 列表定义） |
| **FXName** | 简短描述或标题（最好不超过 25 个字符） |
| **CreatorID** | 声音设计师、录音师或供应商（或其缩写） |
| **SourceID** | 项目、节目或音效库名称（或其缩写） |

### 2.1 CatID（类别标识）

CatID 以缩写形式同时代表类别（Category）和子类别（SubCategory），定义见通用分类系统列表。

- 它是整个系统的 **核心**——也是使用该系统的唯一硬性要求。
- **不得修改**列表中的 CatID，且必须保留大小写。
- 它确保所有人发布木门音效时都认同其缩写形式为 `DOORWood`。
- 脚本可以将 CatID 解析为 Category 和 SubCategory 字段，并通过查找列表拼接出 `CategoryFull` 字段（例如 `DOORWood` → `DOORS-WOOD`）。

### 2.2 CatShort（类别缩写）

`CatShort` 仅为类别的缩写。目前 **未** 用作元数据字段，也 **不** 用于文件名中——文件名开头必须使用完整的 CatID。它在列表中提供，供未来或用户自行使用。

### 2.3 FXName（音效名称）

文件名中的第二个信息块，可以把它理解为 **标题**。

- 目标：对声音进行简短描述，约 25 个字符较为理想。
- 并非要取代更详尽的"描述"（Description）元数据字段。
- 目的是让用户一眼就能明白这个声音文件是什么，而无需试听。

### 2.4 CreatorID（创作者标识）

标明是谁录制或设计了这个声音。

- 供应商可在此填写名称，个人可填写姓名或缩写。
- 大多数情况下建议使用缩写。
- UCS 有一份供应商列表，允许供应商分配官方缩写。
- 请在所有产品中保持 **一致**。

### 2.5 SourceID（来源标识）

存放节目、项目或音效库的名称或缩写。

- 应包含该声音所属的音效库名称，或其设计/录制所针对的节目名称。
- 如果名称很长，建议使用缩写。

---

## 3. 可选信息块

文件名中还提供三个可选信息块以满足特定场景：**UserCategory**（用户类别）、**VendorCategory**（供应商类别）和 **UserData**（用户数据）。

### 完整文件名结构

```
CatID(-UserCategory)_(VendorCategory-)FXName_CreatorID_SourceID_UserData
```

| 信息块 | 定义 |
|--------|------|
| **UserCategory** | CatID 块的可选尾部扩展，可用作用户自定义类别、麦克风、拾音方位等。 |
| **VendorCategory** | FXName 块的可选头部扩展，供供应商定义音效库专属类别（例如具体枪械、车辆、地点等）。 |
| **UserData** | 用户自定义自由空间，常用于存放 ID/编号以确保文件名 100% 唯一，或存储麦克风类型、地点、方位等。当前不映射到标准元数据，但用户可自行映射到数据库字段。 |

### 3.1 UserCategory（用户类别）

- CatID 的可选 **尾部扩展**，在 CatID 后加连字符 `-` 并追加用户自定义术语或缩写。
- **供应商应避免** 使用此区域。
- 旨在让用户创建自己的"子子类别"（第三级类别）。
- 常见用法：`INT` 和 `EXT` 分别表示室内（INTERIOR）和室外（EXTERIOR）。
- 可定义为缩写并配合查找表使用。

### 3.2 VendorCategory（供应商类别）

- FXName 块的可选 **头部扩展**。
- 定义为紧跟第一个 `_` 之后、直到下一个 `-` 之前的文本块。
- 作为供应商可定义的音效库专属类别，用于在库内部进行组织。
- 可在供应商将现有音效库适配到 UCS 标准时，保留其原有的逻辑分类体系。

### 3.3 UserData（用户数据）

- 文件名结构中的 **最后一个** 信息块，完全自由格式。
- 不分配给任何标准元数据字段——由每个用户/供应商自行决定如何使用。
- 可存储麦克风或方位、唯一文件编号，或任何其他信息。
- 在此块中使用额外下划线虽不推荐，但也不禁止。

---

## 4. 文件名示例

### 示例 1 — 基本结构（有效）

```
GUNAuto_Uzi 9mm Rapid Fire Close Up Short Bursts_TN_DORY
```

- **CatID** = `GUNAuto` → 类别 `GUNS`，子类别 `AUTOMATIC`，完整类别 `GUNS-AUTOMATIC`
- **FXName** = `Uzi 9mm Rapid Fire Close Up Short Bursts`
- **CreatorID** = `TN` → 通过查找表解析为 `Tim Nielsen`
- **SourceID** = `DORY` → 通过查找表解析为项目名 `Finding Dory`（《海底总动员 2：多莉去哪儿》）

在 CatID、CreatorID 和 SourceID 中使用缩写，既能控制文件名长度，又保持可读性。

### 示例 2 — 含 UserData

```
GUNAuto_UZI 9mm Rapid Fire Close Up Short Bursts_TN_DORY_WideStereoMKH8020
```

- 在 **UserData** 块中添加了 `WideStereoMKH8020`。
- 默认不会分配到特定元数据字段，但用户可通过脚本将其映射到自选字段。

### 示例 3 — 含 UserCategory

```
GUNAuto-INT_UZI 9mm Rapid Fire Close Up Short Bursts_TN_DORY
```

- 在 CatID 后直接添加 `-INT`，定义 **UserCategory** = `INT`。
- 工具可将其放入 `UserCategory` 元数据字段（例如麦克风方位、节目专属类别等）。

### 示例 4 — 含 VendorCategory

```
GUNAuto_UZI 9mm-Rapid Fire Close Up Short Bursts_TN_DORY
```

- 未定义 UserCategory，但在 FXName 头部添加 `UZI 9mm-`，从而定义 **VendorCategory** = `UZI 9mm`。
- 第一个和第二个 `_` 之间的整块文本在技术上是 FX Name（`UZI 9mm-Rapid Fire Close Up Short Bursts`），但第一个 `_` 与第一个 `-` 之间的部分同时被定义为 VendorCategory。

### 示例 5 — 完整文件名（所有块均使用）

```
GUNAuto-EXT_UZI 9mm-Rapid Fire Close Up Short Bursts_TN_NONE_416-MKH8040-DualMono
```

| 字段 | 值 |
|------|-----|
| **CatID** | `GUNAuto`（GUNS-AUTOMATIC） |
| **UserCategory** | `EXT`（用户标注为室外录音） |
| **FXName** | `UZI 9mm-Rapid Fire Close Up Short Bursts` |
| **VendorCategory** | `UZI 9mm` |
| **CreatorID** | `TN`（Tim Nielsen 的缩写） |
| **SourceID** | `NONE`（表示并非为特定项目录制） |
| **UserData** | `416-MKH8040-DualMono` |

---

## 5. 总结

UCS 系统的 **唯一硬性要求** 是：

1. 将每个文件指定到列表中的某一个"类别 / 子类别"配对。
2. 将对应的 `CatID_` 放在文件名的 **最开头**。

其余结构完全可选。

### 遵循该要求的直接好处

- 音效库购买者能立即知道该声音属于哪个"类别 / 子类别"配对（例如 `GUNAuto` → `GUNS-AUTOMATIC`）。
- `CatID_` 在文件名开头的固定位置，使脚本能够将信息解析回填到元数据字段。
- 同一"类别 / 子类别"的所有声音会在任何列表、DAW 区域列表或文件夹中自动排在一起。

### 工具支持

目前已有大量工具、脚本和辅助程序可帮助按照此规范命名文件，包括适用于 Pro Tools、Reaper 等 DAW 的工具。更多信息及下载请参见 UCS Google 共享云端硬盘中的 **UTILITIES** 文件夹。
