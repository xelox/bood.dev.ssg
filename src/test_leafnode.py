import unittest
from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        span_node = LeafNode('span', 'hello world!')
        self.assertEqual(span_node.to_html(), '<span>hello world!</span>')

    def test_to_html_with_prop(self):
        a_node = LeafNode(tag='a', value='click here!', props={'href': 'https://www.example.com'})
        self.assertEqual(a_node.to_html(), '<a href="https://www.example.com">click here!</a>')

    def test_no_tag(self):
        no_tag_node = LeafNode(tag=None, value='some value')
        self.assertEqual(no_tag_node.to_html(), "some value")

    def test_to_html_fail(self):
        node = LeafNode(tag='span', value=None)
        self.assertRaises(ValueError, node.to_html)
