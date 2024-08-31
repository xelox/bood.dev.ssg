import unittest
from parentnode import ParentNode
from leafnode import LeafNode


class TestParentNode(unittest.TestCase):
    def test_to_html(self):
        child1 = LeafNode(tag='b', value='1')
        child2 = LeafNode(tag=None, value='2')
        child3 = LeafNode(tag='i', value='3')
        parent_node = ParentNode('span', [child1, child2, child3])
        self.assertEqual(parent_node.to_html(), '<span><b>1</b>2<i>3</i></span>')

    def test_to_html_with_prop(self):
        child1 = LeafNode(tag='b', value='1')
        child2 = LeafNode(tag=None, value='2')
        child3 = LeafNode(tag='i', value='3')
        a_node = ParentNode(
            tag='a',
            children=[child1, child2, child3],
            props={'href': 'https://www.example.com'}
        )
        self.assertEqual(
            a_node.to_html(),
            '<a href="https://www.example.com"><b>1</b>2<i>3</i></a>'
        )

    def test_no_tag(self):
        no_tag_node = ParentNode(tag=None, children='some value')
        self.assertRaises(ValueError, no_tag_node.to_html)

    def test_to_html_fail(self):
        node = ParentNode(tag='span')
        self.assertRaises(ValueError, node.to_html)
