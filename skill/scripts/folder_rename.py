#!/usr/bin/env python3
"""
UCS 文件夹批量重命名映射生成器 v2
修正: CatShort-level GENERAL -> 用 Category 名; 天气/归档多 CatShort 处理; 小船/枪支手动映射
"""
import os
import csv
import json
from collections import defaultdict

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TSV_PATH = os.path.join(SKILL_DIR, "references", "ucs-zh-en.tsv")
ROOT_DIR = "D:/UCS音效库文件夹"

def load_tsv(path):
    rows = []
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            rows.append(row)
    return rows

def build_lookups(rows):
    cat_zh_map = defaultdict(list)
    subcat_lookup = {}
    catshort_zh_map = defaultdict(list)
    for r in rows:
        cat_zh = r['Category_zh'].strip()
        subcat_zh = r['SubCategory_zh'].strip()
        cat = r['Category'].strip()
        subcat = r['SubCategory'].strip()
        cat_id = r['CatID'].strip()
        cat_short = r['CatShort'].strip()
        cat_zh_map[cat_zh].append(r)
        subcat_lookup[(cat_zh, subcat_zh)] = (cat, subcat, cat_id, cat_short)
        if cat_id == cat_short:
            catshort_zh_map[cat_zh].append(r)
    return cat_zh_map, subcat_lookup, catshort_zh_map

def title_case_english(name):
    parts = name.split()
    result = []
    for p in parts:
        if p == '&':
            result.append('&')
        else:
            sub_parts = p.split('-')
            result.append('-'.join(s.capitalize() if s != '&' else s for s in sub_parts))
    return ' '.join(result)

def get_dir_tree(root):
    dirs = []
    for dirpath, dirnames, filenames in os.walk(root):
        for d in sorted(dirnames):
            full = os.path.join(dirpath, d)
            rel = os.path.relpath(full, root)
            dirs.append((rel, full))
    return dirs

# 手动映射: 不在 UCS 对照表或需要特殊处理的文件夹
MANUAL_MAP = {
    "小船": ("Boats", "手动映射: 小船 -> Boats (不在 UCS 表，归入 BOATS)"),
    "小船/舱内": ("Interior", "手动映射: 小船/舱内 -> BOATS INTERIOR"),
    "枪支": ("Guns", "手动映射: 枪支 -> Guns (UCS 表中为'枪炮')"),
    "枪支/操作": ("Handle", "手动映射: 枪支/操作 -> GUNS HANDLE"),
}

def generate_rename_mapping(rows):
    cat_zh_map, subcat_lookup, catshort_zh_map = build_lookups(rows)
    all_dirs = get_dir_tree(ROOT_DIR)
    unmatched = []
    renames = []

    for rel_path, full_path in all_dirs:
        parts = rel_path.replace('\\', '/').split('/')
        current_zh = parts[-1]

        # 先检查手动映射
        if rel_path.replace('\\', '/') in MANUAL_MAP:
            eng, info = MANUAL_MAP[rel_path.replace('\\', '/')]
            eng_title = title_case_english(eng)
            new_name = f"【{current_zh}】{eng_title}"
            renames.append((rel_path, new_name, eng_title, info))
            continue

        if len(parts) == 1:
            # 顶层目录
            entries = cat_zh_map.get(current_zh, [])
            catshort_entries = catshort_zh_map.get(current_zh, [])

            if catshort_entries:
                # 检查所有 CatShort 条目是否属于同一 Category
                cats = set(e['Category'] for e in catshort_entries)
                if len(cats) == 1:
                    e = catshort_entries[0]
                    if len(catshort_entries) == 1 and e['SubCategory'].strip() == 'GENERAL':
                        # CatShort-level with GENERAL subcat -> use Category name
                        eng = e['Category'].strip()
                        eng_title = title_case_english(eng)
                        new_name = f"【{current_zh}】{eng_title}"
                        renames.append((rel_path, new_name, eng_title, f"CatShort GENERAL: {e['CatID']} -> {e['Category']}"))
                    elif len(catshort_entries) == 1:
                        # CatShort-level, use SubCategory name
                        eng = e['SubCategory'].strip()
                        eng_title = title_case_english(eng)
                        new_name = f"【{current_zh}】{eng_title}"
                        renames.append((rel_path, new_name, eng_title, f"CatShort-level: {e['CatID']}"))
                    else:
                        # 多个 CatShort 条目同一 Category -> use Category name
                        eng = e['Category'].strip()
                        eng_title = title_case_english(eng)
                        new_name = f"【{current_zh}】{eng_title}"
                        renames.append((rel_path, new_name, eng_title, f"Multi-CatShort, Cat={e['Category']}"))
                else:
                    unmatched.append((rel_path, f"多个不同 Category 的 CatShort: {cats}"))
            elif len(entries) == 1:
                e = entries[0]
                eng = e['Category'].strip()
                eng_title = title_case_english(eng)
                new_name = f"【{current_zh}】{eng_title}"
                renames.append((rel_path, new_name, eng_title, f"Category: {e['Category']}"))
            elif len(entries) > 1:
                cats = set(e['Category'] for e in entries)
                if len(cats) == 1:
                    e = entries[0]
                    eng = e['Category'].strip()
                    eng_title = title_case_english(eng)
                    new_name = f"【{current_zh}】{eng_title}"
                    renames.append((rel_path, new_name, eng_title, f"Category: {e['Category']}"))
                else:
                    unmatched.append((rel_path, f"多个不同 Category: {cats}"))
            else:
                unmatched.append((rel_path, "无 Category 匹配"))

        elif len(parts) == 2:
            parent_zh = parts[0]
            key = (parent_zh, current_zh)
            parent_catshort_entries = catshort_zh_map.get(parent_zh, [])

            if parent_catshort_entries and len(parent_catshort_entries) == 1 and current_zh == parent_zh:
                # 同名子文件夹 (呼呼声/呼呼声, 嗖嗖声/嗖嗖声)
                parent_entry = parent_catshort_entries[0]
                eng = parent_entry['SubCategory'].strip()
                eng_title = title_case_english(eng)
                new_name = f"【{current_zh}】{eng_title}"
                renames.append((rel_path, new_name, eng_title, f"CatShort sub: {parent_entry['CatID']}"))
            else:
                match = subcat_lookup.get(key)
                if match:
                    cat, subcat, cat_id, cat_short = match
                    # SubCategory 为 GENERAL 时，英文用 Category 名
                    if subcat == 'GENERAL':
                        eng_title = title_case_english(cat)
                    else:
                        eng_title = title_case_english(subcat)
                    new_name = f"【{current_zh}】{eng_title}"
                    renames.append((rel_path, new_name, eng_title, f"SubCat: {cat_id}"))
                else:
                    # 检查 SubCategory_zh 含 "/" 的拆分情况
                    parent_entries = cat_zh_map.get(parent_zh, [])
                    found = False
                    for e in parent_entries:
                        sc_zh = e['SubCategory_zh'].strip()
                        if '/' in sc_zh and current_zh in sc_zh.split('/'):
                            eng = e['SubCategory'].strip()
                            eng_title = title_case_english(eng)
                            new_name = f"【{current_zh}】{eng_title}"
                            renames.append((rel_path, new_name, eng_title, f"Split SubCat: {e['CatID']}"))
                            found = True
                            break
                    if not found:
                        unmatched.append((rel_path, f"无 SubCategory 匹配 (parent={parent_zh})"))

        elif len(parts) == 3:
            parent_zh = parts[0]
            mid_zh = parts[1]
            current_zh = parts[2]
            combined_zh = f"{mid_zh}/{current_zh}"
            key = (parent_zh, combined_zh)
            match = subcat_lookup.get(key)
            if match:
                cat, subcat, cat_id, cat_short = match
                eng_title = title_case_english(subcat)
                new_name = f"【{current_zh}】{eng_title}"
                renames.append((rel_path, new_name, eng_title, f"Deep SubCat: {cat_id}"))
            else:
                unmatched.append((rel_path, f"3级目录未匹配"))
        else:
            unmatched.append((rel_path, f"深度 {len(parts)} 级目录"))

    return renames, unmatched

def main():
    rows = load_tsv(TSV_PATH)
    renames, unmatched = generate_rename_mapping(rows)

    print(f"=== 匹配结果 ===")
    print(f"成功匹配: {len(renames)}")
    print(f"未匹配:  {len(unmatched)}")
    print()

    if unmatched:
        print("=== 未匹配目录 ===")
        for path, reason in unmatched:
            print(f"  {path}  -- {reason}")
        print()

    # 检查格式问题
    format_issues = []
    for rel_path, new_name, eng, info in renames:
        if eng == "General":
            format_issues.append((rel_path, new_name, "英文为 General，应使用 Category 名"))
        if not new_name.startswith("【"):
            format_issues.append((rel_path, new_name, "缺少【】格式"))

    if format_issues:
        print("=== 格式问题 ===")
        for path, name, issue in format_issues:
            print(f"  {path} -> {name}  -- {issue}")
        print()

    # 输出完整映射
    print("=== 重命名映射 (原路径 TAB 新名) ===")
    for rel_path, new_name, eng, info in renames:
        print(f"{rel_path}\t{new_name}")

    # 保存 JSON
    output = {
        "matched": [{"path": r[0], "new_name": r[1], "english": r[2], "info": r[3]} for r in renames],
        "unmatched": [{"path": u[0], "reason": u[1]} for u in unmatched]
    }
    out_path = os.path.join(SKILL_DIR, "scripts", "rename_mapping.json")
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"\n映射已保存到: {out_path}")

if __name__ == '__main__':
    main()
