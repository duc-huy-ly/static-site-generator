import unittest
from textnode import TextNode, TextType
from md_to_text_node import *

class TestSplitNodesDelimiter(unittest.TestCase):
    
    def test_split_nodes_delimiter_basic_bold(self):
        """Test basic bold text splitting"""
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_split_nodes_delimiter_basic_italic(self):
        """Test basic italic text splitting"""
        node = TextNode("This is text with an *italic* word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        
        expected = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_split_nodes_delimiter_basic_code(self):
        """Test basic code text splitting"""
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_split_nodes_delimiter_multiple_occurrences(self):
        """Test multiple occurrences of the same delimiter"""
        node = TextNode("This has **bold** and **more bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        expected = [
            TextNode("This has ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("more bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_split_nodes_delimiter_no_delimiter(self):
        """Test text with no delimiter remains unchanged"""
        node = TextNode("This is just plain text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        expected = [TextNode("This is just plain text", TextType.TEXT)]
        self.assertEqual(new_nodes, expected)
    
    def test_split_nodes_delimiter_multiple_nodes(self):
        """Test splitting multiple nodes"""
        nodes = [
            TextNode("First **bold** text", TextType.TEXT),
            TextNode("Second node with **bold**", TextType.TEXT),
        ]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        
        expected = [
            TextNode("First ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
            TextNode("Second node with ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_split_nodes_delimiter_non_text_nodes_unchanged(self):
        """Test that non-TEXT nodes are passed through unchanged"""
        nodes = [
            TextNode("Normal text with **bold**", TextType.TEXT),
            TextNode("Already bold", TextType.BOLD),
            TextNode("Already italic", TextType.ITALIC),
        ]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        
        expected = [
            TextNode("Normal text with ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode("Already bold", TextType.BOLD),
            TextNode("Already italic", TextType.ITALIC),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_split_nodes_delimiter_empty_segments_skipped(self):
        """Test that empty segments between delimiters are skipped"""
        node = TextNode("Text with ****empty**** delimiters", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("empty", TextType.TEXT),
            TextNode(" delimiters", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_split_nodes_delimiter_at_start_and_end(self):
        """Test delimiter at the start and end of text"""
        node = TextNode("**bold start** and **bold end**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        expected = [
            TextNode("bold start", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("bold end", TextType.BOLD),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_split_nodes_delimiter_only_formatted_text(self):
        """Test text that is entirely formatted"""
        node = TextNode("**entirely bold**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        expected = [TextNode("entirely bold", TextType.BOLD)]
        self.assertEqual(new_nodes, expected)
    
    def test_split_nodes_delimiter_unmatched_raises_exception(self):
        """Test that unmatched delimiters raise an exception"""
        node = TextNode("This has **unmatched delimiter", TextType.TEXT)
        
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(str(context.exception), "Unmatched delimiter")
    
    def test_split_nodes_delimiter_empty_list(self):
        """Test with empty list of nodes"""
        new_nodes = split_nodes_delimiter([], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [])
    
    def test_split_nodes_delimiter_empty_text(self):
        """Test with empty text node"""
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        expected = [TextNode("", TextType.TEXT)]
        self.assertEqual(new_nodes, expected)
    
    def test_split_nodes_delimiter_consecutive_delimiters(self):
        """Test consecutive delimiters"""
        node = TextNode("**bold****italic** text", TextType.TEXT)
        # First split for bold
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode("italic", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_split_nodes_delimiter_complex_text(self):
        """Test complex text with multiple formatting"""
        node = TextNode("Start **bold** middle *italic* end `code` finish", TextType.TEXT)
        # Split for bold first
        nodes_after_bold = split_nodes_delimiter([node], "**", TextType.BOLD)
        # Then split for italic
        nodes_after_italic = split_nodes_delimiter(nodes_after_bold, "*", TextType.ITALIC)
        # Finally split for code
        final_nodes = split_nodes_delimiter(nodes_after_italic, "`", TextType.CODE)
        
        expected = [
            TextNode("Start ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" middle ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" end ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" finish", TextType.TEXT),
        ]
        self.assertEqual(final_nodes, expected)

class TestExtractImage(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
        
    def test_extract_markdown_link(self):
        matches = extract_markdown_link(
            """This is a link [my link](https://i.imgur.com/zjjcJKZ.png). Here is an image ![img](random.io)
            Here is a final link [click me!!!](valve.com)"""
        )
        self.assertListEqual([("my link", "https://i.imgur.com/zjjcJKZ.png"),("click me!!!", "valve.com")], matches)
if __name__ == "__main__":
    unittest.main()