import os
import re
import json
import json5  # pip install json5

# === CONFIG ===
input_file = "Syllabus.txt"   # file đầu vào (.txt)
output_dir = "output_json"
os.makedirs(output_dir, exist_ok=True)

# === ĐỌC FILE ===
with open(input_file, "r", encoding="utf-8") as f:
    content = f.read()

# === TÌM CÁC KHỐI JSON ===
# Hỗ trợ mọi dạng tiêu đề: P1_U2_LReview 1_SY / P1_U4_LTest: 1A (Listening, Reading, Writing)_SY
pattern = r"--\s*\d+\.\s*([^\n-]+?)\s*--\s*\{(.*?)\}(?=\s*(--|$))"
matches = re.findall(pattern, content, flags=re.DOTALL)

print(f"🔍 Found {len(matches)} JSON blocks\n")

# === HÀM PARSE AN TOÀN ===
def safe_parse_json(json_text: str):
    """
    Parse JSON, tự động sửa lỗi các chuỗi chứa dấu " hoặc '
    """
    # Thử parse bằng json5 (linh hoạt hơn)
    try:
        return json5.loads(json_text)
    except Exception:
        pass

    # Nếu vẫn lỗi, thử tự động escape các dấu " trong value
    escaped = re.sub(
        r'(".*?":\s*")(.*?)(?<!\\)"(.*?")', 
        lambda m: m.group(1) + m.group(2).replace('"', '\\"') + m.group(3),
        json_text
    )

    try:
        return json.loads(escaped)
    except Exception:
        return None

# === GHI TỪNG FILE ===
for idx, (raw_name, json_body, _) in enumerate(matches, start=1):
    file_name = raw_name.strip()
    json_text = "{" + json_body.strip() + "}"

    data = safe_parse_json(json_text)

    # Làm sạch tên file (tránh ký tự không hợp lệ trong hệ thống)
    safe_name = re.sub(r'[\\/:*?"<>|]', "_", file_name)
    output_path = os.path.join(output_dir, f"{safe_name}.json")

    if data is None:
        # Nếu vẫn lỗi → lưu file raw để bạn debug
        raw_path = os.path.join(output_dir, f"{safe_name}.json")
        with open(raw_path, "w", encoding="utf-8") as f:
            f.write(json_text)
        print(f"⚠️  Could not parse JSON (saved raw): {file_name}")
        continue

    # Ghi file JSON đã sửa
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✅ Created: {safe_name}.json")

print("\n🎉 All JSON files generated successfully!")
