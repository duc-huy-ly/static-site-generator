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
        
        node2 = TextNode("bad `code block`` here", TextType.TEXT)
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter([node2], "`", TextType.CODE)
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
        
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

class TestSplitNodesImage(unittest.TestCase):
    def test_split_nodes_image_single_image(self):
        """Test splitting a single image from text"""
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_image_multiple_images(self):
        """Test splitting multiple images from text"""
        node = TextNode(
            "Start ![first](url1.png) middle ![second](url2.png) end",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("Start ", TextType.TEXT),
            TextNode("first", TextType.IMAGE, "url1.png"),
            TextNode(" middle ", TextType.TEXT),
            TextNode("second", TextType.IMAGE, "url2.png"),
            TextNode(" end", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_image_image_at_start(self):
        """Test image at the beginning of text"""
        node = TextNode(
            "![logo](logo.png) welcome text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("logo", TextType.IMAGE, "logo.png"),
            TextNode(" welcome text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_image_image_at_end(self):
        """Test image at the end of text"""
        node = TextNode(
            "Text with image ![final](final.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("Text with image ", TextType.TEXT),
            TextNode("final", TextType.IMAGE, "final.png"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_image_only_image(self):
        """Test text containing only an image"""
        node = TextNode("![solo](solo.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [TextNode("solo", TextType.IMAGE, "solo.png")]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_image_no_images(self):
        """Test text with no images"""
        node = TextNode("This is plain text with no images", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [TextNode("This is plain text with no images", TextType.TEXT)]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_image_non_text_nodes_unchanged(self):
        """Test that non-TEXT nodes are passed through unchanged"""
        nodes = [
            TextNode("Text ![img](url.png)", TextType.TEXT),
            TextNode("Already an image", TextType.IMAGE, "url.png"),
        ]
        new_nodes = split_nodes_image(nodes)
        expected = [
            TextNode("Text ", TextType.TEXT),
            TextNode("img", TextType.IMAGE, "url.png"),
            TextNode("Already an image", TextType.IMAGE, "url.png"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_image_multiple_nodes(self):
        """Test splitting multiple nodes"""
        nodes = [
            TextNode("First ![image1](url1.png)", TextType.TEXT),
            TextNode("Second ![image2](url2.png)", TextType.TEXT),
        ]
        new_nodes = split_nodes_image(nodes)
        expected = [
            TextNode("First ", TextType.TEXT),
            TextNode("image1", TextType.IMAGE, "url1.png"),
            TextNode("Second ", TextType.TEXT),
            TextNode("image2", TextType.IMAGE, "url2.png"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_image_empty_list(self):
        """Test with empty list of nodes"""
        new_nodes = split_nodes_image([])
        self.assertEqual(new_nodes, [])

    def test_split_nodes_image_empty_text(self):
        """Test with empty text node"""
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [TextNode("", TextType.TEXT)]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_image_consecutive_images(self):
        """Test consecutive images with no text between them"""
        node = TextNode("![first](url1.png)![second](url2.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("first", TextType.IMAGE, "url1.png"),
            TextNode("second", TextType.IMAGE, "url2.png"),
        ]
        self.assertEqual(new_nodes, expected)

class TestSplitNodesLink(unittest.TestCase):
    def test_split_nodes_link_single_link(self):
        """Test splitting a single link from text"""
        node = TextNode(
            "This is text with a [link](https://www.example.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("link", TextType.IMAGE, "https://www.example.com"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_link_multiple_links(self):
        """Test splitting multiple links from text"""
        node = TextNode(
            "Start [first](url1.com) middle [second](url2.com) end",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("Start ", TextType.TEXT),
            TextNode("first", TextType.IMAGE, "url1.com"),
            TextNode(" middle ", TextType.TEXT),
            TextNode("second", TextType.IMAGE, "url2.com"),
            TextNode(" end", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_link_link_at_start(self):
        """Test link at the beginning of text"""
        node = TextNode(
            "[home](home.com) welcome text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("home", TextType.IMAGE, "home.com"),
            TextNode(" welcome text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_link_link_at_end(self):
        """Test link at the end of text"""
        node = TextNode(
            "Text with link [click here](https://example.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("Text with link ", TextType.TEXT),
            TextNode("click here", TextType.IMAGE, "https://example.com"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_link_only_link(self):
        """Test text containing only a link"""
        node = TextNode("[solo](solo.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [TextNode("solo", TextType.IMAGE, "solo.com")]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_link_no_links(self):
        """Test text with no links"""
        node = TextNode("This is plain text with no links", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [TextNode("This is plain text with no links", TextType.TEXT)]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_link_non_text_nodes_unchanged(self):
        """Test that non-TEXT nodes are passed through unchanged"""
        nodes = [
            TextNode("Text [link](url.com)", TextType.TEXT),
            TextNode("Already a link", TextType.IMAGE, "url.com"),
        ]
        new_nodes = split_nodes_link(nodes)
        expected = [
            TextNode("Text ", TextType.TEXT),
            TextNode("link", TextType.IMAGE, "url.com"),
            TextNode("Already a link", TextType.IMAGE, "url.com"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_link_multiple_nodes(self):
        """Test splitting multiple nodes"""
        nodes = [
            TextNode("First [link1](url1.com)", TextType.TEXT),
            TextNode("Second [link2](url2.com)", TextType.TEXT),
        ]
        new_nodes = split_nodes_link(nodes)
        expected = [
            TextNode("First ", TextType.TEXT),
            TextNode("link1", TextType.IMAGE, "url1.com"),
            TextNode("Second ", TextType.TEXT),
            TextNode("link2", TextType.IMAGE, "url2.com"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_link_empty_list(self):
        """Test with empty list of nodes"""
        new_nodes = split_nodes_link([])
        self.assertEqual(new_nodes, [])

    def test_split_nodes_link_empty_text(self):
        """Test with empty text node"""
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [TextNode("", TextType.TEXT)]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_link_consecutive_links(self):
        """Test consecutive links with no text between them"""
        node = TextNode("[first](url1.com)[second](url2.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("first", TextType.IMAGE, "url1.com"),
            TextNode("second", TextType.IMAGE, "url2.com"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_link_ignores_images(self):
        """Test that image syntax is not treated as links"""
        node = TextNode(
            "Text with ![image](img.png) and [link](link.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("Text with ![image](img.png) and ", TextType.TEXT),
            TextNode("link", TextType.IMAGE, "link.com"),
        ]
        self.assertEqual(new_nodes, expected)

class TestTextToTextNode(unittest.TestCase):
    def test_text_to_text_node_plain_text(self):
        """Test plain text with no formatting"""
        result = text_to_text_node("This is plain text")
        expected = [TextNode("This is plain text", TextType.TEXT)]
        self.assertEqual(result, expected)

    def test_text_to_text_node_bold(self):
        """Test text with bold formatting"""
        result = text_to_text_node("This is **bold** text")
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_text_to_text_node_italic(self):
        """Test text with italic formatting"""
        result = text_to_text_node("This is *italic* text")
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_text_to_text_node_code(self):
        """Test text with code formatting"""
        result = text_to_text_node("This is `code` text")
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_text_to_text_node_image(self):
        """Test text with image"""
        result = text_to_text_node("Text with ![alt](url.png)")
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("alt", TextType.IMAGE, "url.png"),
        ]
        self.assertEqual(result, expected)

    def test_text_to_text_node_link(self):
        """Test text with link"""
        result = text_to_text_node("Text with [link](https://example.com)")
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("link", TextType.IMAGE, "https://example.com"),
        ]
        self.assertEqual(result, expected)

    def test_text_to_text_node_multiple_formats(self):
        """Test text with multiple formatting types"""
        result = text_to_text_node("**bold** and *italic* and `code`")
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("code", TextType.CODE),
        ]
        self.assertEqual(result, expected)

    def test_text_to_text_node_complex(self):
        """Test complex text with bold, italic, code, images, and links"""
        result = text_to_text_node("**bold** text with *italic* and `code` plus ![image](img.png) and [link](url.com)")
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode(" text with ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" plus ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "img.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("link", TextType.IMAGE, "url.com"),
        ]
        self.assertEqual(result, expected)

    def test_text_to_text_node_empty_string(self):
        """Test with empty string"""
        result = text_to_text_node("")
        expected = [TextNode("", TextType.TEXT)]
        self.assertEqual(result, expected)

    def test_text_to_text_node_only_bold(self):
        """Test text that is entirely bold"""
        result = text_to_text_node("**entirely bold**")
        expected = [TextNode("entirely bold", TextType.BOLD)]
        self.assertEqual(result, expected)

    def test_text_to_text_node_nested_delimiters(self):
        """Test text with consecutive formatting"""
        result = text_to_text_node("**bold** *italic* and more")
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode(" ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and more", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_text_to_text_node_image_and_link(self):
        """Test text with both image and link"""
        result = text_to_text_node("![image](img.png) and [link](url.com)")
        expected = [
            TextNode("image", TextType.IMAGE, "img.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("link", TextType.IMAGE, "url.com"),
        ]
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()