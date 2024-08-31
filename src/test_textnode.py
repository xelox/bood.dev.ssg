import unittest

from textnode import TextNode
from leafnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_dif_type_neq(self):
        node = TextNode("This is a text node", "bold")
        second = TextNode("This is a text node", "italic")
        self.assertNotEqual(node, second)

    def test_dif_text_neq(self):
        node = TextNode("Text 1", "bold")
        second = TextNode("Text 2", "bold")
        self.assertNotEqual(node, second)

    def test_to_leafnode_plain(self):
        text = TextNode('Some Plain String', 'text')
        self.assertEqual(text.to_html_node().to_html(), 'Some Plain String')

    def test_to_leafnode_bold(self):
        text = TextNode('Some Bold String', 'bold')
        self.assertEqual(text.to_html_node().to_html(), '<b>Some Bold String</b>')

    def test_to_leafnode_italic(self):
        text = TextNode('Some Italic String', 'italic')
        self.assertEqual(text.to_html_node().to_html(), '<i>Some Italic String</i>')


    def test_to_leafnode_code(self):
        text = TextNode('Some Code String', 'code')
        self.assertEqual(text.to_html_node().to_html(), '<code>Some Code String</code>')

    def test_to_leafnode_link(self):
        text = TextNode('Some Link', 'link', url='https://example.com')
        self.assertEqual(text.to_html_node().to_html(), '<a href="https://example.com">Some Link</a>')

    def test_to_leafnode_image(self):
        text = TextNode('Some Image', 'image', url='https://example.com')
        self.assertEqual(text.to_html_node().to_html(), '<img alt="Some Image" href="https://example.com"></img>')

    def test_to_leafnode_other(self):
        text = TextNode('Some bad text type', 'other')
        self.assertRaises(ValueError, text.to_html_node)

if __name__ == "__main__":
    unittest.main()
