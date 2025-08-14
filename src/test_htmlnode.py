import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        node = HTMLNode(tag='a', props={"href": "https://www.google.com", "target": "_blank",})
        self.assertEqual(repr(node), "HTMLNode(a, None, None, {'href': 'https://www.google.com', 'target': '_blank'})")

    def test_to_html(self):
        node = HTMLNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_props_to_html(self):
        node = HTMLNode(tag='a', props={"href": "https://www.google.com", "target": "_blank",})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')
    
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')
    
    def test_leaf_to_html_value_error(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()
    
    def test_leaf_to_html_label_none(self):
        node = LeafNode(None, "Click me!")
        self.assertEqual(node.to_html(), "Click me!")
    
    def test_repr_leaf(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(repr(node), "LeafNode(a, Click me!, {'href': 'https://www.google.com'})")

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

    def test_parent_repr(self):
        child_node = LeafNode('b', 'child')
        node = ParentNode("span", [child_node])
        self.assertEqual(repr(node), f"ParentNode(span, ['LeafNode(b, child, None)'], None)")

    def test_parent_no_children_to_html(self):
        node = ParentNode('b', None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_parent_no_tag_to_html(self):
        child_node = LeafNode('div', 'child')
        parent_node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_parent_multiple_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_parent_nested_multiple(self):
        child_1 = LeafNode('i', 'child_1')
        child_2 = LeafNode('div', 'child_2')
        child_3 = LeafNode('span', 'child_3')
        parent_1 = ParentNode('div', [child_1])
        parent_2 = ParentNode('span', [child_2, child_3])
        grandparent = ParentNode('b', [parent_1, parent_2])
        self.assertEqual(grandparent.to_html(), '<b><div><i>child_1</i></div><span><div>child_2</div><span>child_3</span></span></b>')
  


if __name__ == "__main__":
    unittest.main()