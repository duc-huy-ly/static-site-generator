from textnode import *
from typing import List, Tuple
import re

"""
Functions that turn a block of text into a list of text nodes
Searches for bold, italic, code, images and links
"""
def text_to_text_node(text : str) -> List[TextNode]:
    initial_text_node = TextNode(text, TextType.TEXT)
    x_0 = split_nodes_delimiter([initial_text_node], "**", TextType.BOLD)
    x_1 = split_nodes_delimiter(x_0, '*', TextType.ITALIC)
    x_2 = split_nodes_delimiter(x_1, '`', TextType.CODE)
    x_3 = split_nodes_image(x_2)
    x_4 = split_nodes_link(x_3)
    return x_4

# The two functions below return a list of key value pairs, the alt text follow by their respective links
def extract_markdown_images(text : str) -> List[Tuple[str, str]]:
    """
    From a given a text, returns a list of dictionnaries that represent a markdown image.
    beginning of para ![alt text](image.jpg) lipsum sola => ("lalt text":"image.jpg",) 
    """
    img_regex = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(img_regex, text)
    return matches

def extract_markdown_link(text : str) -> List[Tuple[str, str]]:
    #  	[title](https://www.example.com)
    link_regex = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(link_regex, text)



def split_nodes_delimiter(old_nodes: List[TextNode], delimiter: str, text_type: TextType) -> List[TextNode]:
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

def split_nodes_image(old_nodes : List[TextNode]) -> List[TextNode]:
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

def split_nodes_link(old_nodes : List[TextNode]) -> List[TextNode]:
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
