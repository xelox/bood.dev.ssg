import unittest

from textnode import TextNode, split_delimiter, split_link, md_to_textnodes
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

    def test_from_md(self):
        test = TextNode("This is *text* with a `code block` word", 'text')
        output1 = split_delimiter([test], '`', 'code')
        expected1 = [
            TextNode("This is *text* with a ", 'text'),
            TextNode('code block', 'code'),
            TextNode(' word', 'text')
        ]

        self.assertEqual(output1, expected1)

        output2 = split_delimiter(output1, '*', 'bold')
        expected2 = [
            TextNode("This is ", 'text'),
            TextNode('text', 'bold'),
            TextNode(' with a ', 'text'),
            TextNode('code block', 'code'),
            TextNode(' word', 'text')
        ]

        self.assertEqual(output2, expected2)

    def test_split_image(self):
        md = TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", 'text')
        expected = [
            TextNode('This is text with a ', 'text'),
            TextNode('rick roll', 'image', 'https://i.imgur.com/aKaOqIh.gif'),
            TextNode(' and ', 'text'),
            TextNode('obi wan', 'image', 'https://i.imgur.com/fJRm4Vk.jpeg'),
        ]
        self.assertEqual(split_link([md], 'image'), expected)

    def test_split_link(self):
        md = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev). The end.", 'bold')
        expected = [
            TextNode('This is text with a link ', 'bold'),
            TextNode('to boot dev', 'link', 'https://www.boot.dev'),
            TextNode(' and ', 'bold'),
            TextNode('to youtube', 'link', 'https://www.youtube.com/@bootdotdev'),
            TextNode('. The end.', 'bold')
        ]
        self.assertEqual(split_link([md], 'link'), expected)

    def test_split_image_and_bold(self):
        md = TextNode("This is text with a *link* [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev). The end.", 'text')
        step1 = split_link([md], 'link')
        step2 = split_delimiter(step1, '*', 'bold')

        expected = [
            TextNode('This is text with a ', 'text'),
            TextNode('link', 'bold'),
            TextNode(' ', 'text'),
            TextNode('to boot dev', 'link', 'https://www.boot.dev'),
            TextNode(' and ', 'text'),
            TextNode('to youtube', 'link', 'https://www.youtube.com/@bootdotdev'),
            TextNode('. The end.', 'text')
        ]

        self.assertEqual(step2, expected)

    def test_md_to_textnodes(self):
        self.maxDiff = None

        md = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected = [
            TextNode("This is ", 'text'),
            TextNode("text", 'bold'),
            TextNode(" with an ", 'text'),
            TextNode("italic", 'italic'),
            TextNode(" word and a ", 'text'),
            TextNode("code block", 'code'),
            TextNode(" and an ", 'text'),
            TextNode("obi wan image", 'image', "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", 'text'),
            TextNode("link", 'link', "https://boot.dev"),
        ]
        self.assertEqual(md_to_textnodes(md), expected)

if __name__ == "__main__":
    unittest.main()
