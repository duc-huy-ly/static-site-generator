import unittest
from handling_blocks import *

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
        codeblock_simple = "```print('Yes Luca')```"
        self.assertEqual(block_to_block_type(codeblock_simple), cb)
        codeblock_simple2 = "```print('Yes')\necho\nokay```"
        self.assertEqual(block_to_block_type(codeblock_simple2), cb)
        
        multi_line = """```
for i in range(10):
print(i)
```"""
        self.assertEqual(block_to_block_type(multi_line), cb)
        
    def test_bad_code_block(self):
        sample2="``Missing```"
        self.assertEqual(block_to_block_type(sample2), BlockType.PARA) 

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
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

if __name__ == "__main__":
    unittest.main()