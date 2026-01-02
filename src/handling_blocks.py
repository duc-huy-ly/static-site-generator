import enum


def markdown_to_blocks(doc : str) -> []:
    """
    Takes raw markdown string and turns it into a list of blocks of string.
    """
    # blocks are seperations of different sections of a doc, denoted by a single blank line
    sections = list(filter(None, doc.split('\n\n')))
    # Remove trailing whitespaces
    result = [s.strip() for s in sections ]
    return result    
