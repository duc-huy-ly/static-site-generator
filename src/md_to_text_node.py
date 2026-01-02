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
        
# The two functions below return a list of key value pairs, the alt text follow by their respective links
def extract_markdown_images(text):
    # ![alt text](image.jpg)
    img_regex = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(img_regex, text)
    return matches

def extract_markdown_link(text):
    #  	[title](https://www.example.com)
    link_regex = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(link_regex, text)


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue

        list_of_matches = extract_markdown_images(node.text)
        # we have a list of tuples of image matches
        if not list_of_matches:
            new_nodes.append(node)
            continue
        current_text = node.text
        # still have to split the node
        for (alt, url) in list_of_matches:
            # build the string    
            pattern = f"![{alt}]({url})"      
            before, after = current_text.split(pattern, 1) 
            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))
            current_text = after
        # add the final element
        if current_text != "":
            new_nodes.append(TextNode(current_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue

        list_of_matches = extract_markdown_link(node.text)
        # we have a list of tuples of image matches
        if not list_of_matches:
            new_nodes.append(node)
            continue
        current_text = node.text
        # still have to split the node
        for (alt, url) in list_of_matches:
            # build the string    
            pattern = f"[{alt}]({url})"      
            before, after = current_text.split(pattern, 1) 
            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))
            current_text = after
        # this is the remainder 
        if current_text != "":
            new_nodes.append(TextNode(current_text, TextType.TEXT))
    return new_nodes