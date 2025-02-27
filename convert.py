import sys
import os
import markdown
import yaml  # 需要安装 PyYAML

def convert_md_to_html(md_filepath):
    with open(md_filepath, 'r', encoding='utf-8') as f:
        md_text = f.read()
    metadata = {}
    # 检查是否存在 YAML 前置元数据
    if md_text.startswith('---'):
        parts = md_text.split('---', 2)
        if len(parts) >= 3:
            raw_meta = parts[1]
            md_text = parts[2]
            try:
                metadata = yaml.safe_load(raw_meta) or {}
            except Exception as e:
                print(f"Error parsing YAML metadata: {e}")
    # 使用扩展支持 fenced code block，并指定输出格式为 html5
    html = markdown.markdown(md_text, 
                               extensions=['fenced_code', 'codehilite', 'tables', 'toc'],
                               output_format='html5')
    # 注入许可协议信息
    license_html = "<div class='license'><p>许可协议<br>CC BY-NC-SA 4.0</p></div>\n"
    # 构造 head 元素
    head_meta = "<meta charset='utf-8'>\n"
    title = metadata.get('title', os.path.basename(md_filepath))
    if metadata.get('description'):
        head_meta += f"<meta name='description' content='{metadata.get('description')}'>\n"
    if metadata.get('tags'):
        tags = metadata.get('tags')
        if isinstance(tags, list):
            tags_str = ','.join(tags)
        else:
            tags_str = tags
        head_meta += f"<meta name='keywords' content='{tags_str}'>\n"
    if metadata.get('published'):
        head_meta += f"<meta name='date' content='{metadata.get('published')}'>\n"
    if metadata.get('category'):
        head_meta += f"<meta name='category' content='{metadata.get('category')}'>\n"
    # 添加内嵌CSS，使图片适应视窗
    css = "<style>img { max-width: 100%; height: auto; } pre, code { white-space: pre-wrap; }</style>\n"
    # 构造用于显示所有元数据的 HTML 片段
    meta_html = "<div id='metadata'>\n"
    for key, value in metadata.items():
        meta_html += f"<p><strong>{key.capitalize()}:</strong> {value}</p>\n"
    meta_html += "</div>\n"
    # 在元数据与正文之间插入 <hr>
    meta_html += "<hr>\n"
    # 读取 footer.html 内容
    footer_html = ""
    footer_path = os.path.join(os.getcwd(), "html", "footer.html")
    if os.path.exists(footer_path):
        with open(footer_path, "r", encoding="utf-8") as f:
            footer_html = f.read()
    # 模板暂时留空，可引入 template 下的 CSS
    html_output = ("<!DOCTYPE html>\n<html>\n<head>\n" +
                   head_meta +
                   f"<title>{title}</title>\n" +
                   "<!-- 可引入模板CSS -->\n" +
                   css +
                   "</head>\n<body>\n" +
                   meta_html +    # 插入元数据展示
                   html +
                   license_html + # 注入许可协议信息
                   footer_html +  # 注入 footer.html 内容
                   "\n</body>\n</html>")
    return html_output

def process_file(md_filepath, output_dir):
    html_output = convert_md_to_html(md_filepath)
    html_filename = os.path.splitext(os.path.basename(md_filepath))[0] + ".html"
    html_filepath = os.path.join(output_dir, html_filename)
    with open(html_filepath, "w", encoding="utf-8") as f:
        f.write(html_output)
    print(f"Converted {md_filepath} to {html_filepath}")

if __name__ == "__main__":
    # 定义相关目录
    posts_dir = os.path.join(os.getcwd(), "posts")
    html_dir = os.path.join(os.getcwd(), "html")
    template_dir = os.path.join(os.getcwd(), "template")  # 暂时留空，不做处理

    # 自动创建 html 输出目录（如不存在）
    if not os.path.exists(html_dir):
        os.makedirs(html_dir)

    if len(sys.argv) < 2:
        if not os.path.exists(posts_dir):
            print(f"Directory {posts_dir} does not exist.")
            sys.exit(1)
        for file in os.listdir(posts_dir):
            if file.endswith('.md'):
                md_filepath = os.path.join(posts_dir, file)
                process_file(md_filepath, html_dir)
    else:
        # 处理传入的文件参数（输出位置保持原有逻辑，即同目录下生成html）
        for md_filepath in sys.argv[1:]:
            if not os.path.exists(md_filepath):
                print(f"File {md_filepath} does not exist.")
                continue
            process_file(md_filepath, os.path.dirname(md_filepath))
