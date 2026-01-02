from html_node import *
import unittest

class TestHTMLNode(unittest.TestCase):
    def testCreate(self):
        node = HTMLNode()
        assert(isinstance(node, HTMLNode))
        
    def testPropsToHTML(self):
        node = HTMLNode("a", "Leroy", props={"href": "betterCallSaul.abq", "target":"locked"})
        expected = ' href="betterCallSaul.abq" target="locked"'
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
        
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
    )
    
    def test_parent_node_no_tag_raises_error(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError, msg="All Parent Nodes must have at tag"):
            parent_node.to_html()

    def test_parent_node_empty_children_raises_error(self):
        parent_node = ParentNode("div", [])
        with self.assertRaises(ValueError, msg="Must have children"):
            parent_node.to_html()

    def test_parent_node_none_children_raises_error(self):
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError, msg="Must have children"):
            parent_node.to_html()
    
    def test_parent_with_mixed_children_types(self):
        leaf_child = LeafNode("span", "text")
        parent_child = ParentNode("p", [LeafNode("em", "emphasized")])
        parent_node = ParentNode("div", [leaf_child, parent_child])
        expected = "<div><span>text</span><p><em>emphasized</em></p></div>"
        self.assertEqual(parent_node.to_html(), expected)

    def test_parent_with_multiple_leaf_children(self):
        child1 = LeafNode("span", "first")
        child2 = LeafNode("span", "second")
        child3 = LeafNode("em", "third")
        parent_node = ParentNode("div", [child1, child2, child3])
        expected = "<div><span>first</span><span>second</span><em>third</em></div>"
        self.assertEqual(parent_node.to_html(), expected)
    
    def test_deeply_nested_parent_nodes(self):
        # Level 4: grandgrandchild
        level4 = LeafNode("strong", "deep text")
        
        # Level 3: grandchild
        level3 = ParentNode("em", [level4])
        
        # Level 2: child
        level2 = ParentNode("p", [level3])
        
        # Level 1: parent
        level1 = ParentNode("div", [level2])
        
        expected = "<div><p><em><strong>deep text</strong></em></p></div>"
        self.assertEqual(level1.to_html(), expected)
        
    def test_parent_with_text_only_leaf_children(self):
        # LeafNode with no tag returns just the value
        text_only_child = LeafNode(None, "raw text")
        parent_node = ParentNode("p", [text_only_child])
        expected = "<p>raw text</p>"
        self.assertEqual(parent_node.to_html(), expected)

    def test_parent_with_mixed_text_and_tagged_children(self):
        text_child = LeafNode(None, "Plain text ")
        tagged_child = LeafNode("strong", "bold text")
        parent_node = ParentNode("p", [text_child, tagged_child])
        expected = "<p>Plain text <strong>bold text</strong></p>"
        self.assertEqual(parent_node.to_html(), expected)

    def test_parent_with_siblings_at_different_levels(self):
        # Create a complex tree structure
        leaf1 = LeafNode("span", "text1")
        leaf2 = LeafNode("strong", "text2")
        leaf3 = LeafNode("em", "text3")
        
        inner_parent = ParentNode("p", [leaf2, leaf3])
        root_parent = ParentNode("div", [leaf1, inner_parent])
        
        expected = "<div><span>text1</span><p><strong>text2</strong><em>text3</em></p></div>"
        self.assertEqual(root_parent.to_html(), expected)

    def test_parent_node_with_props(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node], {"class": "container", "id": "main"})
        expected = '<div class="container" id="main"><span>child</span></div>'
        self.assertEqual(parent_node.to_html(), expected)

    def test_parent_node_with_empty_props(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node], {})
        expected = "<div><span>child</span></div>"
        self.assertEqual(parent_node.to_html(), expected)

    def test_parent_node_initialization_defaults(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.tag, "div")
        self.assertEqual(parent_node.value, None)
        self.assertEqual(parent_node.children, [child_node])
        self.assertEqual(parent_node.props, None)
        
    def test_parent_node_repr(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node], {"class": "test"})
        repr_str = repr(parent_node)
        # Should include the tag, children, and props info
        self.assertIn("div", repr_str)
        self.assertIn("child", repr_str)
        self.assertIn("class", repr_str)

    def test_parent_with_many_children(self):
        # Test with a large number of children
        children = [LeafNode("span", f"child_{i}") for i in range(10)]
        parent_node = ParentNode("div", children)
        expected_children = "".join([f"<span>child_{i}</span>" for i in range(10)])
        expected = f"<div>{expected_children}</div>"
        self.assertEqual(parent_node.to_html(), expected)
        
if __name__ == "__main__":
    unittest.main()