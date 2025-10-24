import os
import json
from jinja2 import Environment, FileSystemLoader

# script python render_lesson.py
# Mục đích: Đọc các file JSON trong thư mục json_syllabus và render thành file HTML sử dụng template Jinja2

# Thư mục
JSON_DIR = "json_syllabus" # Thư mục chứa file JSON
OUTPUT_DIR = "output_syllabus_html" # Thư mục xuất file HTML
TEMPLATE_FILE = "syllabus_with_data_fields.jinja2.html" # File template Jinja2

# Tạo folder output nếu chưa có
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Setup Jinja2
env = Environment(loader=FileSystemLoader("."))
template = env.get_template(TEMPLATE_FILE)

# Duyệt tất cả file .json trong thư mục json_files
for file_name in os.listdir(JSON_DIR):
    if not file_name.endswith(".json"):
        continue

    json_path = os.path.join(JSON_DIR, file_name)
    print(f"🔄 Processing {json_path} ...")

    try:
        # Đọc JSON
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            # nếu JSON là list thì lấy phần tử đầu
            if isinstance(data, list):
                data = data[0]

        # Render HTML
        html_output = template.render(**data)

        # Xuất file
        output_name = os.path.splitext(file_name)[0] + ".html"
        output_path = os.path.join(OUTPUT_DIR, output_name)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_output)

        print(f"✅ Done -> {output_path}")

    except Exception as e:
        print(f"❌ Error processing {file_name}: {e}")

print("\n🎉 All JSON files processed successfully!")
