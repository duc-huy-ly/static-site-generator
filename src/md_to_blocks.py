from enum import Enum
from html_node import *
from textnode import *
from md_to_text_node import *
import re
""" 
In our simple markdown parser, we are not allowed to put blank lines inside the code blocks. The parsing done is very simplistic by splitting the original document (string) with the \n\n delimiter.
Inserting blank lines inside code blocks will split the code block.


"""

class BlockType(Enum):
    HEADING = 1
    CODEBLOCK = 2
    QUOTEBLOCK = 3
    ULIST = 4
    OLIST = 5
    PARA = 6

def block_to_block_type(block: str) -> BlockType :
    lines = block.split("\n")
    if re.search(r"(^#{1,6} )", block) :
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODEBLOCK
    # multi line case
    if all(line.startswith('>') for line in lines):
        return BlockType.QUOTEBLOCK
    if all(line.startswith('- ') for line in lines):
        return BlockType.ULIST
    # Check if the ordered list rule is followed
    for i in range(len(lines)):
        # if we find an error, set the block to paragraph (last case)
        if not lines[i].startswith(f"{i + 1}."): # start from 1
            return BlockType.PARA
    # All checks passed
    return BlockType.OLIST
    

def markdown_to_blocks(doc : str) -> []:
    """
    Takes raw markdown string and turns it into a list of blocks of string.
    """
    # blocks are seperations of different sections of a doc, denoted by a single blank line
    sections = list(filter(None, doc.split('\n\n')))
    # Remove trailing whitespaces
    result = [s.strip() for s in sections ]
    return result    

def markdown_to_html_node(doc : str) -> HTMLNode:
    root = ParentNode("div", children=[])
    for text_block in markdown_to_blocks(doc):
        # print(text_block)
        type = block_to_block_type(text_block)
        if type == BlockType.CODEBLOCK :
            wrapper = ParentNode("pre", [LeafNode("code", text_block.strip("```"))])
            root.children.append(wrapper)
            # root.children.append(LeafNode("code", text_block.strip("```")))
        elif type == BlockType.ULIST:
            ulist_elements = []
            for line in text_block.split("\n") :
                ulist_elements.append(ParentNode("li", text_to_children(line.strip("- "))))
            root.children.append(ParentNode("ul", ulist_elements))
        elif type == BlockType.OLIST:
            olist_elements = []
            for line in text_block.split("\n"):
                # Remove the numbering system, values on the right part of the line
                olist_elements.append(ParentNode("li", text_to_children(line.strip(". ")[1])))
            root.children.append(ParentNode("ol", olist_elements))
        elif type == BlockType.HEADING:
            number_of_hashes = 0
            for i in range(0, 6):
                if text[i] != "#":
                    break
                number_of_hashes += 1
            hashes = "#"*number_of_hashes+" "
            root.children.append(LeafNode(f"h{number_of_hashes}", text_block.strip(hashes)))
        elif type == BlockType.QUOTEBLOCK:
            root.children.append(ParentNode("blockquote", text_to_children(text_block.strip('> '))))
        else:
            html_node_of_text_block = ParentNode("p", text_to_children(text_block))
            root.children.append(html_node_of_text_block)
    return root

def text_to_children(inline):
    """ Transforms a inline text to a list of LeafNodes"""
    root = []
    text_nodes = text_to_text_node(inline)
    for text_node in text_nodes:
        root.append(text_node_to_html_node(text_node))
    return root
            
    
def determine_tag_type(text, type ):
    if type == BlockType.HEADING:
        number_of_hashes = 0
        for i in range(0, 6):
            if text[i] != "#":
                break
            number_of_hashes += 1
        return f"h{number_of_hashes}"
    if type == BlockType.ULIST:
        return "ul"
    if type == BlockType.OLIST:
        return "ol"
    if type == BlockType.CODEBLOCK:
        return "pre"
    if type == BlockType.QUOTEBLOCK:
        return "blockquote"
    else :
        return "p"

md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with *italic* text and `print('hello world')` here

"""
md2 = """
hello 

```
This is text that _should_ remain
the **same** even with inline stuff
```

another one. 
Bites the buts

"""
# print(markdown_to_html_node(md).to_html())
print(markdown_to_html_node(md2).to_html())
