import unittest
from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        node = LeafNode('span', 'hello world!');
        self.assertEqual(node.to_html(), '<span>hello world!</span>')

    def test_to_html_with_prop(self):
        node = LeafNode(tag='a', value='click here!', props={'href': 'https://www.example.com'});
        self.assertEqual(node.to_html(), '<a href="https://www.example.com">click here!</a>');

    def test_to_html_fail(self):
        node = LeafNode(tag='span', value=None)
        with self.assertRaises(ValueError):
            node.to_html()

        node2 = LeafNode(tag='span', value='hello world!', children={'some':'data'})
        with self.assertRaises(ValueError):
            node2.to_html()
