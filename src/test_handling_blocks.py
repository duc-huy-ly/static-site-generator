import unittest
from handling_blocks import markdown_to_blocks

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


if __name__ == "__main__":
    unittest.main()