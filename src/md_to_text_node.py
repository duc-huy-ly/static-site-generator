from textnode import *
import re

def split_nodes_delimiter(old_nodes: [], delimiter: str, text_type: TextType) -> []:
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue
        parts = node.text.split(delimiter)
        
        if len(parts) == 1:
            new_nodes.append(node)
            continue
    
        if len(parts) % 2 == 0:
            raise Exception("Unmatched delimiter")
        
        for index, part in enumerate(parts):
            if part == "":
                continue  
            if index %2 ==0:
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))
    return new_nodes
        
def extract_markdown_images(text):
    # ![alt text](image.jpg)
    img_regex = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(img_regex, text)
    return matches

def extract_markdown_link(text):
    #  	[title](https://www.example.com)
    link_regex = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(link_regex, text)

