import os
import json
from bs4 import BeautifulSoup

# === CONFIG ===
TEMPLATE_FILE = "lession_plan.html"  # template HTML có data-type / data-field
JSON_DIR = "json_lessionPlan"                 # thư mục JSON input
OUTPUT_DIR = "output__lession_plan_html"      # thư mục output HTML

os.makedirs(OUTPUT_DIR, exist_ok=True)


def fill_element(element, data, path="root"):
    """Đệ quy: điền data vào DOM dựa trên data-field / data-type"""
    if data is None:
        return

    field = element.get("data-field")
    dtype = element.get("data-type")

    # Nếu có data-field
    if field:
        value = None
        if isinstance(data, dict):
            value = data.get(field)

        if dtype == "string":
            if value is None:
                return
            if element.strong:
                element.strong.insert_after(" " + str(value))
            else:
                element.string = str(value)

        elif dtype == "object":
            if not isinstance(value, dict):
                # in cảnh báo nếu sai cấu trúc
                print(f"⚠️ [{path}.{field}] expected object, got {type(value).__name__}")
                return
            for child in element.find_all(attrs={"data-field": True}, recursive=False):
                fill_element(child, value, f"{path}.{field}")

        elif dtype == "array":
            if not isinstance(value, list):
                print(f"⚠️ [{path}.{field}] expected array, got {type(value).__name__}")
                return
            template_item = element.find(attrs={"data-item": "true"})
            if not template_item:
                print(f"⚠️ [{path}.{field}] no data-item template found")
                return
            template_html = str(template_item)
            template_item.decompose()

            for idx, item in enumerate(value):
                item_soup = BeautifulSoup(template_html, "html.parser")
                fill_element(item_soup, item, f"{path}.{field}[{idx}]")
                element.append(item_soup)

    else:
        # Nếu không có data-field thì đi tiếp vào các con
        for child in element.find_all(attrs={"data-field": True}, recursive=False):
            fill_element(child, data, path)


def render_html(template_path, json_path, output_path):
    with open(template_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    root = soup.find(attrs={"data-field": "root"})
    if not root:
        raise ValueError("❌ Không tìm thấy phần tử data-field='root' trong template")

    # Nếu JSON không có key 'root' thì thêm tạm
    if "root" not in data:
        data = {"root": data}

    fill_element(root, data, "root")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(str(soup))


# === MAIN ===
for file_name in os.listdir(JSON_DIR):
    if not file_name.endswith(".json"):
        continue

    json_path = os.path.join(JSON_DIR, file_name)
    output_path = os.path.join(OUTPUT_DIR, file_name.replace(".json", ".html"))

    print(f"🔄 Rendering {file_name} ...")
    try:
        render_html(TEMPLATE_FILE, json_path, output_path)
        print(f"✅ Done -> {output_path}")
    except Exception as e:
        print(f"❌ Error processing {file_name}: {e}")

print("\n🎉 All JSON files processed successfully!")
