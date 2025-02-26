import os
import datetime
import xml.etree.ElementTree as ET

def generate_sitemap():
    base_url = "https://www.onani.cn/"  # 请替换为你的实际站点域名
    html_dir = os.path.join(os.getcwd(), "html")
    excluded_files = ["footer.html"]
    urlset = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    for filename in os.listdir(html_dir):
        if filename.endswith('.html') and filename.lower() not in excluded_files:
            file_path = os.path.join(html_dir, filename)
            last_mod = datetime.datetime.fromtimestamp(os.path.getmtime(file_path)).strftime("%Y-%m-%d")
            url = ET.SubElement(urlset, "url")
            loc = ET.SubElement(url, "loc")
            loc.text = base_url + "html/" + filename
            lastmod = ET.SubElement(url, "lastmod")
            lastmod.text = last_mod
    sitemap_path = os.path.join(html_dir, "sitemap.xml")
    tree = ET.ElementTree(urlset)
    tree.write(sitemap_path, encoding="utf-8", xml_declaration=True)
    print("Sitemap generated at", sitemap_path)

if __name__ == "__main__":
    generate_sitemap()
