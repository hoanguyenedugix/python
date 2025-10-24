import os

# Đường dẫn tới thư mục chứa JSON và HTML
json_folder = r"./json_syllabus"
html_folder = r"./output_syllabus_html"

# Lấy danh sách file trong mỗi thư mục
json_files = sorted([f for f in os.listdir(json_folder) if f.endswith(".json")])
html_files = sorted([f for f in os.listdir(html_folder) if f.endswith(".html")])

# Kiểm tra độ dài 2 danh sách để tránh lỗi
if len(json_files) != len(html_files):
    print(f"Số lượng file không khớp! JSON: {len(json_files)}, HTML: {len(html_files)}")
else:
    for json_file, html_file in zip(json_files, html_files):
        # Lấy tên file HTML (bỏ phần mở rộng)
        new_name = os.path.splitext(html_file)[0] + ".json"
        
        old_path = os.path.join(json_folder, json_file)
        new_path = os.path.join(json_folder, new_name)
        
        os.rename(old_path, new_path)
        print(f"✅ Đã đổi: {json_file}  →  {new_name}")

print("🎯 Hoàn thành đổi tên!")
