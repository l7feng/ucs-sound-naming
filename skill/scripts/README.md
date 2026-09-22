# scripts（文件夹批量重命名工具）

配套 UCS 文件夹批量重命名的两个脚本，把一个中文命名的音效库目录树改成 UCS 格式。

| 文件 | 作用 |
|---|---|
| `folder_rename.py` | 生成映射：扫描目标目录树，比对 `../references/ucs-zh-en.tsv`，产出 `rename_mapping.json` |
| `folder_rename_exec.py` | 执行重命名：读映射，从最深层目录开始逐级改名（默认 dry-run，需显式确认才落盘） |
| `rename_mapping.json` | 生成的映射表（`matched` / `unmatched` 两组） |

两个脚本里的 `ROOT_DIR` 是默认库路径，按需改成自己的路径再运行。执行前建议先 dry-run 核对。
