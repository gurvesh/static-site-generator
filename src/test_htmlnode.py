import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from textnode import TextNode, TextType

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        html1 = HTMLNode(props={
            "href": "https://www.google.com",
            "target": "_blank",
        })
        val = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(val, html1.props_to_html())

    def test_props_to_html2(self):
        html1 = HTMLNode()
        val = ''
        self.assertEqual(val, html1.props_to_html())
    
    def test_props_to_html2(self):
        html2 = HTMLNode(props={"x": 56})
        self.assertEqual(html2.props_to_html(), ' x="56"')

    def test_repr(self):
        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(tag: p, value: What a strange world, children: None, props: {'class': 'primary'})",
        )
    
    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_raw(self):
        node = LeafNode(None, "raw text")
        self.assertEqual(node.to_html(), "raw text")

class TestParentNode(unittest.TestCase):
    def test_parent_to_html_error_no_tag(self):
        node = ParentNode(None, ['something'])
        self.assertRaises(ValueError, node.to_html)

    def test_parent_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_parent_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_to_html_recursive(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        )
        node2 = ParentNode(
            "p",
            [
                node,
                LeafNode("i", "something")
            ],
        )
        self.assertEqual(
            node2.to_html(),
            f"<p>{node.to_html()}<i>something</i></p>"    
        )

class TextFuncTextNodeToHTML(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is bold text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), '<b>This is bold text node</b>')

    def test_img(self):
        node = TextNode("Click here", TextType.LINK, url="https://google.com")
        html_node = LeafNode("a", "Click here", props={"href": "https://google.com"})
        html_text = '<a href="https://google.com">Click here</a>'
        self.assertEqual(text_node_to_html_node(node).to_html(), html_node.to_html())
        self.assertEqual(text_node_to_html_node(node).to_html(), html_text)

if __name__ == "__main__":
    unittest.main()