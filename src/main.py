from textnode import *
import os
import shutil
from md_to_blocks import markdown_to_html_node

def main():
    copy_files("static/", "public/")
    generate_page("content/index.md", "template.html", "public")
    return 0
    
def copy_files(src, dst, is_root=True):
    if os.path.exists(dst) and is_root:
        shutil.rmtree(dst)
    if is_root:
        os.mkdir(dst)
    contents = os.listdir(src)
    # print(contents)
    for content in contents:
        src_path = os.path.join(src, content)
        dst_path = os.path.join(dst, content)
        if os.path.isfile(src_path):
            shutil.copy(src_path, dst_path)
        elif os.path.isdir(src_path):
            os.mkdir(dst_path)
            copy_files(src_path, dst_path, is_root=False)
    # shutil.copytree(src, dst)     
    
def extract_title(markdown):
    lines = list(filter(None, markdown.split("\n")))
    for line in lines:
        if line.strip().startswith("# "):
            return line.split("# ",1)[1]          
    
def generate_page(src_path, template_path, dst_path):
    print(f"Generating page from {src_path} to {dst_path} using {template_path}")
    src_md = open(src_path).read()
    template_html = open(template_path).read()
    src_html = markdown_to_html_node(src_md).to_html()
    
    title = extract_title(src_md)
    endfile = template_html.replace("{{ Content }}", src_html).replace("{{ Title }}", title)

    # filepath = os.path.join(dst_path, f"{title}.html")
    if not os.path.exists(dst_path):
        os.makedirs(dst_path)
    file_name = src_path.split('/')[-1].split('.')[0]
    with open(os.path.join(dst_path, f"{file_name}.html"), "x") as f:
        f.write(endfile)
    
if __name__ == '__main__':
    main()
    
