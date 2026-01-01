import unittest

from textnode import TextNode, TextType


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

if __name__ == "__main__":
    unittest.main()