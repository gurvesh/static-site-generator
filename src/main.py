from textnode import TextNode, TextType
from blocks import markdown_to_html_node
import os
import shutil
import re
import sys

def main():
    # dummy_node = TextNode("This is some anchor text", TextType.ANCHOR_TEXT, "https://www.boot.dev")
    # print(dummy_node)
    if len(sys.argv) < 2:
        basepath = "/"
    else:
        basepath = sys.argv[1]
    cwd = os.getcwd()
    source = os.path.join(cwd, "static")
    dest = os.path.join(cwd, "docs")
    recurse_copy_dir(source, dest)
    md_loc = os.path.join(cwd, "content")
    template_loc = os.path.join(cwd, "template.html")
    dest_path = os.path.join(cwd, "docs")
    generate_page_recursive(md_loc, template_loc, dest_path, basepath)


def recurse_copy_dir(source, dest):
    if not os.path.exists(source):
        raise Exception(f"please check path: source - {source}")
    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.mkdir(dest)
    for item in os.listdir(source):
        item_full_loc = os.path.join(source, item)
        if os.path.isfile(item_full_loc):
            print(f"Copying: {item_full_loc} to {dest}")
            shutil.copy(item_full_loc, dest)
        elif os.path.isdir(item_full_loc):
            new_source = item_full_loc
            new_dest = os.path.join(dest, item)
            recurse_copy_dir(new_source, new_dest)

def extract_title(markdown):
    lines = markdown.splitlines()
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("Title not found! Document must have a title")

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    full_md = ""
    template = ""
    title = ""
    
    with open(from_path, 'r') as f:
        full_md = f.read()
        title = extract_title(full_md)

    with open(template_path, 'r') as f:
        template = f.read()
    
    node = markdown_to_html_node(full_md)
    html = node.to_html()

    full_html = template.replace("{{ Title }}", title)
    full_html = full_html.replace("{{ Content }}", html)
    full_html = full_html.replace('href="/', f'href="{basepath}')
    full_html = full_html.replace('src="/', f'src="{basepath}')

    with open(dest_path, 'w+') as f:
        f.write(full_html)

def generate_page_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    if not os.path.exists(dir_path_content):
        raise Exception(f"please check path: dir_path_content: {dir_path_content}")
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)
    for item in os.listdir(dir_path_content):
        item_full_loc = os.path.join(dir_path_content, item)
        if os.path.isfile(item_full_loc):
            item_name = item.split(".")[0]
            dest_item_name = item_name + ".html"
            full_dest = os.path.join(dest_dir_path, dest_item_name)
            generate_page(item_full_loc, template_path, full_dest, basepath)
        elif os.path.isdir(item_full_loc):
            new_dir_path_content = item_full_loc
            new_dest_dir_path = os.path.join(dest_dir_path, item)
            generate_page_recursive(new_dir_path_content, template_path, new_dest_dir_path, basepath)

main()