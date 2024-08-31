import unittest

from textnode import TextNode


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


if __name__ == "__main__":
    unittest.main()
