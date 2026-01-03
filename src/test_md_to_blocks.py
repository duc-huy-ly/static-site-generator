import unittest
from md_to_blocks import *

class TestMDtoHTML(unittest.TestCase):
    def test_determine_tag(self):
        string = "# Heading"
        string2 = "## Heading"
        string3 = "###### Heading"
        self.assertEqual(determine_tag_type(string, BlockType.HEADING), "h1")
        self.assertEqual(determine_tag_type(string2, BlockType.HEADING), "h2")
        self.assertEqual(determine_tag_type(string3, BlockType.HEADING), "h6")
        bad1 = "# #Heading"
        self.assertEqual(determine_tag_type(bad1, BlockType.HEADING), "h1")
        bad2 = "### #Heading"
        self.assertEqual(determine_tag_type(bad2, BlockType.HEADING), "h3")
        
        

class TestIdentifyBlockType(unittest.TestCase):
    def test_heading_correst(self):
        x = "# yes"
        block_x = block_to_block_type(x)
        self.assertEqual(block_x, BlockType.HEADING)
        self.assertEqual(block_to_block_type('## yes'), BlockType.HEADING)
        self.assertEqual(block_to_block_type('#### yes'), BlockType.HEADING)
        self.assertEqual(block_to_block_type('##### yes'), BlockType.HEADING)
        self.assertEqual(block_to_block_type('###### yes'), BlockType.HEADING)
        self.assertEqual(block_to_block_type('####### 7 is the limit'), BlockType.PARA)
        self.assertEqual(block_to_block_type('#No gap'), BlockType.PARA)
        multi_line = """ # start
        nest
        """
        self.assertEqual(block_to_block_type(multi_line), BlockType.PARA)
        
    def test_detect_code_block(self):
        cb = BlockType.CODEBLOCK
        codeblock_simple = "```\nprint('Yes Luca')\n```"
        self.assertEqual(block_to_block_type(codeblock_simple), cb)
        codeblock_simple2 = "```\nprint('Yes')\necho\nokay\n```"
        self.assertEqual(block_to_block_type(codeblock_simple2), cb)
        
        multi_line = """```
for i in range(10):
print(i)
```"""
        md2 = """```
This is text that _should_ remain
the **same** even with inline stuff
```"""
        self.assertEqual(block_to_block_type(multi_line), cb)
        self.assertEqual(block_to_block_type(md2), cb)
                
    def test_bad_code_block(self):
        sample2="``Missing```"
        self.assertEqual(block_to_block_type(sample2), BlockType.PARA) 

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_markdown_to_blocks_with_codeblock(self):
        extract = """
# we start here lads

```
echo('hello')
ls -a
```

end of block
"""
        result = markdown_to_blocks(extract)
        self.assertEqual(result, ["# we start here lads", "```\necho('hello')\nls -a\n```", "end of block"])
    
    def test_single_block(self):
        doc = "This is a single block"
        result = markdown_to_blocks(doc)
        self.assertEqual(result, ["This is a single block"])

    def test_multiple_blocks(self):
        doc = "Block 1\n\nBlock 2\n\nBlock 3"
        result = markdown_to_blocks(doc)
        self.assertEqual(result, ["Block 1", "Block 2", "Block 3"])

    def test_blocks_with_whitespace(self):
        doc = "  Block 1  \n\n  Block 2  "
        result = markdown_to_blocks(doc)
        self.assertEqual(result, ["Block 1", "Block 2"])

    def test_empty_string(self):
        doc = ""
        result = markdown_to_blocks(doc)
        self.assertEqual(result, [])

    def test_only_blank_lines(self):
        doc = "\n\n\n\n"
        result = markdown_to_blocks(doc)
        self.assertEqual(result, [])

    def test_multiline_blocks(self):
        doc = "Line 1\nLine 2\n\nLine 3\nLine 4"
        result = markdown_to_blocks(doc)
        self.assertEqual(result, ["Line 1\nLine 2", "Line 3\nLine 4"])

    def test_blocks_with_internal_whitespace(self):
        doc = "  Block with spaces  \n\n  Another block  "
        result = markdown_to_blocks(doc)
        self.assertEqual(result, ["Block with spaces", "Another block"])
        
    def test_paragraphs_and_code(self):
        corpus = """
Hello world.

```
print('yes')
print('no')
```

Goodbye.
"""
        result = markdown_to_blocks(corpus)
        self.assertEqual(result, ["Hello world.","```\nprint('yes')\nprint('no')\n```", "Goodbye."])
    def test_quote_block(self):
        cb = BlockType.QUOTEBLOCK
        quote_simple = "> This is a quote"
        self.assertEqual(block_to_block_type(quote_simple), cb)
        quote_multi = "> Line 1\n> Line 2\n> Line 3"
        self.assertEqual(block_to_block_type(quote_multi), cb)
        
    def test_unordered_list(self):
        ul = BlockType.ULIST
        ulist_simple = "- Item 1"
        self.assertEqual(block_to_block_type(ulist_simple), ul)
        ulist_multi = "- Item 1\n- Item 2\n- Item 3"
        self.assertEqual(block_to_block_type(ulist_multi), ul)
        
    def test_ordered_list(self):
        ol = BlockType.OLIST
        olist_simple = "1. First"
        self.assertEqual(block_to_block_type(olist_simple), ol)
        olist_multi = "1. First\n2. Second\n3. Third"
        self.assertEqual(block_to_block_type(olist_multi), ol)
        
    def test_ordered_list_invalid(self):
        bad_olist = "0. First\n2. Third"
        self.assertEqual(block_to_block_type(bad_olist), BlockType.PARA)
        bad_olist2 = "0. First\n1. Second"
        self.assertEqual(block_to_block_type(bad_olist2), BlockType.PARA)

    def test_quote_block_invalid(self):
        bad_quote = "> Line 1\nLine 2"
        self.assertEqual(block_to_block_type(bad_quote), BlockType.PARA)

    def test_ulist_invalid(self):
        bad_ulist = "- Item 1\n* Item 2"
        self.assertEqual(block_to_block_type(bad_ulist), BlockType.PARA)
        


class TestTextToChildren(unittest.TestCase):
    def test_text_to_children_plain_text(self):
        result = text_to_children("Hello world")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].tag, None)
        self.assertEqual(result[0].value, "Hello world")
    
    def test_text_to_children_with_bold(self):
        result = text_to_children("This is **bold** text")
        self.assertTrue(len(result) == 3)
        self.assertTrue(any(node.tag == "b" for node in result))
    
    def test_text_to_children_with_italic(self):
        result = text_to_children("This is *italic* text")
        self.assertTrue(len(result) == 3)
        self.assertTrue(any(node.tag == "i" for node in result))
    
    def test_text_to_children_with_code(self):
        result = text_to_children("Use `code` here")
        self.assertTrue(len(result) ==3)
        self.assertTrue(any(node.tag == "code" for node in result))
    
    def test_text_to_children_mixed_formatting(self):
        result = text_to_children("**bold** and *italic* and `code`")
        self.assertTrue(len(result) == 5)
    
    def test_text_to_children_empty_string(self):
        result = text_to_children("")
        self.assertEqual(len(result), 1)
    
    def test_text_to_children_returns_list(self):
        result = text_to_children("Some text")
        self.assertIsInstance(result, list)




if __name__ == "__main__":
    unittest.main()