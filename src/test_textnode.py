import unittest

from textnode import *


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD, "www.google.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "www.google.com")
        self.assertEqual(node, node2)
    
    def test_not_eq_texttype(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node3 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node3)
    
    def test_url_none(self):
        node = TextNode("This is a text node", TextType.BOLD, None)
        node2 = TextNode("This is a text node", TextType.BOLD, None)
        self.assertEqual(node, node2)
        
    def test_not_eq_text(self):
        node = TextNode("This", TextType.ITALIC)
        node3 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node3)
        
    def test_not_eq_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "www.wewinthose.com")
        node3 = TextNode("This is a text node", TextType.ITALIC, "www.gabenewall.valve")
        self.assertNotEqual(node, node3)
    
    def test_text_node_to_str(self):
        node = TextNode("We are number one", TextType.TEXT)
        self.assertEqual(str(node), "TextNode(We are number one, text, None)")
    
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        
    def test_bold_to_html(self):
        node = TextNode("bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'b')
        self.assertEqual(html_node.value, "bold text")
        self.assertEqual(html_node.props, None)

    def test_italic_to_html(self):
        node = TextNode("italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'i')
        self.assertEqual(html_node.value, "italic text")
        self.assertEqual(html_node.props, None)
    
    def test_code_to_html(self):
        node = TextNode("echo('hello world')", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'code')
        self.assertEqual(html_node.value, "echo('hello world')")
        self.assertEqual(html_node.props, None)
        
    def test_link_to_html(self):
        node = TextNode("A random page", TextType.LINKS, "https://jog.example.net/")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'a')
        self.assertEqual(html_node.value, "A random page")
        self.assertEqual(html_node.props, {"href":"https://jog.example.net/"})
    
    def test_image_to_html(self):
        node = TextNode("polish cow image", TextType.IMAGE, "https://i.ytimg.com/vi/9hhMUT2U2L4/mqdefault.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'img')
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src":"https://i.ytimg.com/vi/9hhMUT2U2L4/mqdefault.jpg", "alt":"polish cow image"})
if __name__ == "__main__":
    unittest.main()