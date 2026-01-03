from enum import Enum
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

def block_to_block_type(block: str) :
    if re.search(r"(^#{1,6} )", block) :
        return BlockType.HEADING
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODEBLOCK
    # multi line case
    lines = block.split("\n")
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
