from bs4 import BeautifulSoup
import sys, os

def convert_element(el, path=None, indent=0):
    """Đệ quy chuyển element HTML thành template Jinja"""
    if el.name is None:
        return el  # giữ nguyên text node

    data_type = el.get("data-type")
    data_field = el.get("data-field")
    data_item = el.get("data-item")

    space = " " * indent
    path = path or []
    inner_html = "".join(convert_element(child, path + ([data_field] if data_field else []), indent + 2) for child in el.contents)

    # 1️⃣ Chuỗi đơn giản
    if data_type == "string" and data_field:
        jinja_path = ".".join(path + [data_field])
        return f"{space}{{{{ {jinja_path} }}}}"

    # 2️⃣ Mảng
    elif data_type == "array" and data_field:
        loop_var = data_field.rstrip("s") if data_field.endswith("s") else "item"
        jinja_path = ".".join(path + [data_field])
        return f"{space}{{% for {loop_var} in {jinja_path} %}}\n{inner_html}\n{space}{{% endfor %}}"

    # 3️⃣ Đối tượng
    elif data_type == "object" and data_item:
        loop_var = data_field or "obj"
        jinja_path = ".".join(path)
        return f"{space}{{% for {loop_var} in {jinja_path} %}}\n{inner_html}\n{space}{{% endfor %}}"

    # 4️⃣ Các tag khác
    attrs = " ".join(f'{k}="{v}"' for k, v in el.attrs.items() if not k.startswith("data-"))
    open_tag = f"{space}<{el.name}{(' ' + attrs) if attrs else ''}>"
    close_tag = f"</{el.name}>"
    return f"{open_tag}{inner_html}{close_tag}"

def convert_html_to_jinja(input_html):
    soup = BeautifulSoup(input_html, "html.parser")
    return convert_element(soup.body or soup)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python convert_to_jinja_v2.py input.html output.jinja2.html")
        sys.exit(1)

    input_path, output_path = sys.argv[1], sys.argv[2]

    with open(input_path, "r", encoding="utf-8") as f:
        html = f.read()

    result = convert_html_to_jinja(html)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(result)

    print(f"✅ Converted successfully -> {output_path}")
