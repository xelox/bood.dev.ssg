import unittest

from htmlnode import HTMLNode


class TestTextNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(tag='body', value='Hello World?', props={'cool': 'prop', 'other': 'item'})
        self.assertEqual(node.props_to_html(), ' cool="prop" other="item"')

    def test_repr(self):
        node = HTMLNode(tag='body', value='Hello World?', props={'cool': 'prop', 'other': 'item'})
        self.assertIsInstance(node.__repr__(), str)


if __name__ == "__main__":
    unittest.main()
