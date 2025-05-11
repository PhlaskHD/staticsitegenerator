import unittest
from main import *
from textnode import *
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_is_tag_empty(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
    
    def test_is_value_empty(self):
        node = HTMLNode()
        self.assertIsNone(node.value)

    def test_is_children_empty(self):
        node = HTMLNode()
        self.assertIsNone(node.children)

class TestLeafNode(unittest.TestCase):
    def test_tohtml_test(self):
        node = LeafNode("p", "This is a test",)
        self.assertEqual(node.to_html(), "<p>This is a test</p>")
    
    def test_empty_tag(self):
        node = LeafNode(None, "This is a test")
        self.assertEqual(node.to_html(), "This is a test")

    def test_empty_val(self):
        node = LeafNode("p", None)
        self.assertRaises(ValueError, node.to_html)

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com">Click me!</a>',
        )

class TestParentNode(unittest.TestCase):
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
    
    def test_fuck_my_shit_up_fam(self):
        grandchild1 = LeafNode("b", "grandchild and bold")
        grandchild2 = LeafNode("i", "grandchild and italics")
        grandchild3 = LeafNode(None, "grandchild and no tag")
        child1 = ParentNode("span", [grandchild1, grandchild2])
        child2 = ParentNode("span", [grandchild3])
        parent_node = ParentNode("div", [child1, child2])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild and bold</b><i>grandchild and italics</i></span><span>grandchild and no tag</span></div>"
        )


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

    def test_to_html_many_children(self):
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
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )
    
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_bold(self):
        node = TextNode("big boy indeed", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "big boy indeed")
        self.assertEqual(html_node.to_html(), "<b>big boy indeed</b>")

    def test_image_with_url(self):
        node = TextNode("![a picture of the big boy himself!!!](www.fatdoinks.com)", TextType.IMAGE, "www.fatdoinks.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src":"www.fatdoinks.com", "alt":"a picture of the big boy himself!!!"})
        self.assertEqual(html_node.to_html(), '<img src="www.fatdoinks.com" alt="a picture of the big boy himself!!!"></img>')

class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_image(self):
        node = TextNode("This is an image", TextType.IMAGE, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://www.boot.dev", "alt": "This is an image"},
        )

    def test_bold(self):
        node = TextNode("This is bold", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold")



if __name__ == "__main__":
    unittest.main()
