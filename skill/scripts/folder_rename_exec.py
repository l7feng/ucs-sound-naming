#!/usr/bin/env python3
"""
UCS 文件夹批量重命名执行脚本
从最深层目录开始重命名（避免路径冲突），每个目录只改 basename
"""
import os
import json
import sys
import time

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAPPING_PATH = os.path.join(SKILL_DIR, "scripts", "rename_mapping.json")
ROOT_DIR = "D:/UCS音效库文件夹"

def dry_run():
    """Dry run: 只打印将要执行的操作，不实际重命名"""
    with open(MAPPING_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    matched = data['matched']
    # 按深度排序: 最深的先改
    sorted_items = sorted(matched, key=lambda x: x['path'].count('/') + x['path'].count('\\'), reverse=True)

    rename_ops = []
    for item in sorted_items:
        old_rel = item['path'].replace('\\', '/')
        new_name = item['new_name']
        old_full = os.path.join(ROOT_DIR, old_rel)
        parent = os.path.dirname(old_full)
        new_full = os.path.join(parent, new_name)
        rename_ops.append((old_full, new_full, old_rel, new_name))

    # 检查冲突
    new_names_count = {}
    for old_full, new_full, old_rel, new_name in rename_ops:
        parent = os.path.dirname(new_full)
        key = parent
        if key not in new_names_count:
            new_names_count[key] = []
        new_names_count[key].append((new_name, old_rel))

    conflicts = []
    for parent, items in new_names_count.items():
        names = [i[0] for i in items]
        if len(names) != len(set(names)):
            dups = [n for n in names if names.count(n) > 1]
            conflicts.append((parent, dups, items))

    print(f"=== Dry Run 结果 ===")
    print(f"总重命名操作: {len(rename_ops)}")
    print(f"冲突数: {len(conflicts)}")
    if conflicts:
        print("\n=== 冲突详情 ===")
        for parent, dups, items in conflicts:
            print(f"  目录: {parent}")
            for dup in set(dups):
                affected = [rel for name, rel in items if name == dup]
                print(f"    冲突名: {dup}  来源: {affected}")

    print(f"\n=== 前20条重命名预览 ===")
    for old_full, new_full, old_rel, new_name in rename_ops[:20]:
        old_short = os.path.basename(old_full)
        parent_short = os.path.basename(os.path.dirname(old_full))
        print(f"  {old_rel:40s} -> {new_name}")

    print(f"\n=== 最后5条 ===")
    for old_full, new_full, old_rel, new_name in rename_ops[-5:]:
        print(f"  {old_rel:40s} -> {new_name}")

    return rename_ops, conflicts

def execute_rename(rename_ops):
    """实际执行重命名"""
    success = 0
    failed = []
    for old_full, new_full, old_rel, new_name in rename_ops:
        try:
            if os.path.exists(old_full):
                os.rename(old_full, new_full)
                success += 1
            else:
                failed.append((old_rel, new_name, "源目录不存在"))
        except Exception as e:
            failed.append((old_rel, new_name, str(e)))

    print(f"\n=== 执行结果 ===")
    print(f"成功: {success}")
    print(f"失败: {len(failed)}")
    if failed:
        print("\n=== 失败详情 ===")
        for old_rel, new_name, reason in failed:
            print(f"  {old_rel} -> {new_name}  失败: {reason}")

    return success, failed

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "dry"

    if mode == "dry":
        rename_ops, conflicts = dry_run()
        if conflicts:
            print("\n⚠️ 存在命名冲突，请先解决冲突再执行重命名！")
            return
        print(f"\n无冲突。使用 'execute' 参数执行实际重命名: python folder_rename_exec.py execute")
    elif mode == "execute":
        rename_ops, conflicts = dry_run()
        if conflicts:
            print("\n⚠️ 存在命名冲突，已中止执行！")
            return
        print(f"\n即将执行 {len(rename_ops)} 个重命名操作...")
        confirm = input("确认执行? (y/N): ")
        if confirm.lower() == 'y':
            success, failed = execute_rename(rename_ops)
        else:
            print("已取消。")
    else:
        print(f"未知模式: {mode}. 使用 'dry' 或 'execute'")

if __name__ == '__main__':
    main()
