from textnode import *
import os
import shutil

def main():
    copy_files("static/", "public/")
    return 0

    
def copy_files(src, dst, is_root=True):
    if os.path.exists(dst) and is_root:
        shutil.rmtree(dst)
    if is_root:
        os.mkdir(dst)
    contents = os.listdir(src)
    print(contents)
    for content in contents:
        src_path = os.path.join(src, content)
        dst_path = os.path.join(dst, content)
        if os.path.isfile(src_path):
            shutil.copy(src_path, dst_path)
        elif os.path.isdir(src_path):
            os.mkdir(dst_path)
            copy_files(src_path, dst_path, is_root=False)
            
if __name__ == '__main__':
    main()
    
