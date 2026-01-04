from textnode import *
import os
import shutil
from md_to_blocks import markdown_to_html_node

def main():
    copy_files("static/", "public/")
    generate_page_recursive("content/", "template.html", "public")
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
        
def generate_page_recursive(dir_path_content, template_path, dest_dir_path):
    # Make sure they exist
    check_path([dir_path_content, template_path])
    if not os.path.exists(dest_dir_path):
        os.makedirs(dest_dir_path)
        
    directories = os.listdir(dir_path_content)
    for directory in directories:
        # if it's a markdown file
        content_path = os.path.join(dir_path_content, directory)
        dest_dir_content_path = os.path.join(dest_dir_path, directory)
        if os.path.isfile(content_path) and directory.endswith('.md'):
            # we convert to html and create the file in public
            fd =  open(content_path) 
            file_content = fd.read()
            file_html = markdown_to_html_node(file_content).to_html()
            filename = directory.split('.md')[0] + ".html"
            file_title = extract_title(file_content)
            # Write the content in template
            template_html = open(template_path).read()
            result_html = template_html.replace("{{ Content }}", file_html).replace("{{ Title }}", file_title)
            # Create the new html file in the destination directory
            with open(os.path.join(dest_dir_path, filename),"x") as fd1:
                fd1.write(result_html)
        if os.path.isdir(content_path):
            # recursive call
            generate_page_recursive(content_path, template_path, dest_dir_content_path)
    
def check_path(paths):
    for path in paths:
        if not os.path.exists(path):
            raise Exception(path, " doest not exist")
        
if __name__ == '__main__':
    main()
    
