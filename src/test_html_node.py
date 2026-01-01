from html_node import *
import unittest

class TestHTMLNode(unittest.TestCase):
    def testCreate(self):
        node = HTMLNode()
        assert(isinstance(node, HTMLNode))
        
    def testPropsToHTML(self):
        node = HTMLNode("a", "Leroy", props={"href": "betterCallSaul.abq", "target":"locked"})
        expected = 'href="betterCallSaul.abq" target="locked"'
        self.assertEqual(node.props_to_html(), expected)
    
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_(self):
        node = LeafNode("h1", "Hello, world!", {"href":"loser_bigbang"})
        self.assertEqual(node.to_html(), '<h1 href="loser_bigbang">Hello, world!</h1>')

    def test_multi_props(self):
        button = LeafNode("button", "Submit", props={
            "type": "submit",
            "class": "btn btn-primary", 
            "id": "submit-btn",
        })
        expected = '<button type="submit" class="btn btn-primary" id="submit-btn">Submit</button>'
        self.assertEqual(button.to_html(), expected)