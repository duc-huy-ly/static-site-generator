from enum import Enum
from html_node import *
class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINKS = "links"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})" 
    
def text_node_to_html_node(text_node):
    node_type = text_node.text_type
    if node_type == TextType.TEXT:
        return LeafNode(None, text_node.text )
    if node_type == TextType.BOLD:
        return LeafNode("b", text_node.text )
    if node_type == TextType.ITALIC:
        return LeafNode("i", text_node.text )
    if node_type == TextType.CODE:
        return LeafNode("code", text_node.text )
    if node_type == TextType.LINKS:
        return LeafNode("a", text_node.text, {"href":text_node.url} )
    if node_type == TextType.IMAGE:
        return LeafNode("img", "", {"src":text_node.url, "alt":text_node.text})