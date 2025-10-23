import os

# Đường dẫn đến thư mục chứa các file HTML
folder_path = "./output_syllabus_html"

# Danh sách các tên template mới
prefix = "P2_U"  # Đoạn tiền tố như "P2_U"
suffix = "_SY"  # Đoạn hậu tố như "_SY"
lesson_prefix = "L"  # Tiền tố cho các phần L

# Đổi tên tệp trong thư mục
for i in range(1, 73):  # Từ lesson1 đến lesson72
    old_name = f"lession{i}.html"  # Tên cũ của tệp
    # Cấu trúc tên mới: P2_U1_L1_SY, P2_U2_L2_SY, ...
    new_name = f"{prefix}{(i - 1) // 18 + 1}_{lesson_prefix}{(i - 1) % 18 + 1}{suffix}" 
    # Xử lý theo nhóm
    old_path = os.path.join(folder_path, old_name)
    new_path = os.path.join(folder_path, f"{new_name}.html")
    
    # Đổi tên tệp
    os.rename(old_path, new_path)
    print(f"Đã đổi tên {old_name} thành {new_name}.html")
