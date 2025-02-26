import os
import json
import re

def generate_routes():
    html_dir = os.path.join(os.getcwd(), "html")
    if not os.path.exists(html_dir):
        print(f"Directory {html_dir} does not exist.")
        return

    # 更新排除列表，仅排除 footer.html，不再排除 index.html
    excluded_files = ["footer.html"]

    routes = []
    for filename in os.listdir(html_dir):
        if filename.endswith('.html') and filename.lower() not in excluded_files:
            file_path = os.path.join(html_dir, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            # 提取<title>标签中的标题
            match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
            title = match.group(1) if match else os.path.splitext(filename)[0]
            # 提取<meta name="keywords">作为标签
            match_tags = re.search(r'<meta\s+name=["\']keywords["\']\s+content=["\'](.*?)["\']', content, re.IGNORECASE)
            tags = match_tags.group(1) if match_tags else ""
            # 提取<meta name="category">
            match_category = re.search(r'<meta\s+name=["\']category["\']\s+content=["\'](.*?)["\']', content, re.IGNORECASE)
            category = match_category.group(1) if match_category else ""
            # 提取<meta name="date">作为发布日期
            match_date = re.search(r'<meta\s+name=["\']date["\']\s+content=["\'](.*?)["\']', content, re.IGNORECASE)
            published = match_date.group(1) if match_date else ""
            route = filename  # 使用相对路径
            routes.append({"title": title, "route": route, "tags": tags, "category": category, "published": published})
    # 按 published 降序排序（假设格式为 YYYY-MM-DD）
    routes.sort(key=lambda r: r.get("published", ""), reverse=True)
    json_filepath = os.path.join(html_dir, "routes.json")
    with open(json_filepath, "w", encoding="utf-8") as f:
        json.dump(routes, f, ensure_ascii=False, indent=4)
    print("Generated routes.json in", json_filepath)

if __name__ == "__main__":
    generate_routes()
