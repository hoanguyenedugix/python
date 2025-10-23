#!/usr/bin/env python3
"""
batch_fix_json_quotes.py

Tự động load tất cả file JSON từ thư mục input, fix lỗi dấu " không escape,
và ghi ra thư mục output cùng tên file.
Usage:
    python fix_json_quotes.py input_json output_json
"""

import json
import sys
from pathlib import Path
import argparse
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def try_load_json(text: str):
    try:
        return json.loads(text)
    except Exception:
        return None


def is_closing_context(text: str, pos: int):
    """Heuristic: xác định quote có phải quote đóng không"""
    n = len(text)
    i = pos + 1
    while i < n and text[i].isspace():
        i += 1
    if i >= n:
        return True
    return text[i] in [",", "}", "]", ":"]


def repair_json_text(text: str):
    """Heuristic repair: escape các dấu " không hợp lệ trong chuỗi."""
    out = []
    in_string = False
    escaped = False
    i = 0
    n = len(text)
    while i < n:
        ch = text[i]
        if ch == '"' and not escaped:
            if not in_string:
                in_string = True
                out.append(ch)
            else:
                if is_closing_context(text, i):
                    in_string = False
                    out.append(ch)
                else:
                    out.append('\\\"')
            i += 1
            escaped = False
            continue
        if ch == "\\" and not escaped:
            escaped = True
            out.append(ch)
            i += 1
            continue
        out.append(ch)
        escaped = False
        i += 1
    return "".join(out)


def fix_json_file(input_file: Path, output_file: Path):
    """Đọc 1 file JSON, sửa và ghi ra file output."""
    text = input_file.read_text(encoding="utf-8", errors="replace")
    parsed = try_load_json(text)
    if parsed is not None:
        # hợp lệ sẵn, chỉ ghi lại dạng đẹp
        output_file.write_text(json.dumps(parsed, ensure_ascii=False, indent=2), encoding="utf-8")
        logging.info(f"[OK] {input_file.name} (valid JSON)")
        return True

    fixed = repair_json_text(text)
    parsed2 = try_load_json(fixed)
    if parsed2 is None:
        logging.warning(f"[FAIL] {input_file.name} vẫn không parse được sau khi sửa.")
        output_file.write_text(fixed, encoding="utf-8")
        return False

    output_file.write_text(json.dumps(parsed2, ensure_ascii=False, indent=2), encoding="utf-8")
    logging.info(f"[FIXED] {input_file.name} -> {output_file}")
    return True


def process_folder(input_dir: Path, output_dir: Path):
    """Duyệt toàn bộ folder input, fix từng file .json và ghi ra output."""
    output_dir.mkdir(parents=True, exist_ok=True)
    json_files = list(input_dir.glob("*.json"))
    if not json_files:
        logging.warning(f"Không tìm thấy file .json trong {input_dir}")
        return

    total = len(json_files)
    ok = 0
    for f in json_files:
        out_file = output_dir / f.name
        if fix_json_file(f, out_file):
            ok += 1
    logging.info(f"\n✅ Hoàn tất: {ok}/{total} file hợp lệ hoặc đã sửa thành công.")


def main():
    parser = argparse.ArgumentParser(description="Fix unescaped quotes in all JSON files from input folder.")
    parser.add_argument("input_dir", help="Thư mục chứa các file JSON gốc")
    parser.add_argument("output_dir", help="Thư mục để lưu JSON đã fix")
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)

    if not input_dir.exists():
        logging.error(f"Input folder {input_dir} không tồn tại.")
        sys.exit(1)

    process_folder(input_dir, output_dir)


if __name__ == "__main__":
    main()
