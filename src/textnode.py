from leafnode import LeafNode
import re


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    def __eq__(self, other):
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def to_html_node(self) -> LeafNode:
        match self.text_type:
            case 'text':
                return LeafNode(value=self.text)
            case 'bold':
                return LeafNode(tag='b', value=self.text)
            case 'italic':
                return LeafNode(tag='i', value=self.text)
            case 'code':
                return LeafNode(tag='code', value=self.text)
            case 'link':
                return LeafNode(tag='a', value=self.text, props={'href':self.url})
            case 'image':
                return LeafNode(tag='img', props={'alt':self.text, 'href':self.url})
            case _:
                raise ValueError('invalid text type')


    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

def split_delimiter(old_nodes, delimiter: str, text_type: str) -> [LeafNode]:
    res = []
    for node in old_nodes:
        for idx, str_val in enumerate(node.text.split(delimiter)):
            if idx % 2 == 1:
                res.append(TextNode(str_val, text_type))
            else:
                res.append(TextNode(str_val, node.text_type, url=node.url))
    return res

def split_link(old_nodes, link_type):
    pattern = r''
    match link_type:
        case 'link':
            pattern = r'\[(.*?)\]\((.*?)\)'
        case 'image':
            pattern = r'!\[(.*?)\]\((.*?)\)'
        case _:
            raise ValueError('invalid link type')

    res = []
    for node in old_nodes:
        prv_start = 0
        for item in re.finditer(pattern, node.text):
            left_seg = node.text[prv_start:item.start()]
            res.append(TextNode(left_seg, node.text_type))
            alt = item.group(1)
            url = item.group(2)
            res.append(TextNode(alt, link_type, url))
            prv_start = item.end()

        if prv_start != len(node.text):
            last_segment = node.text[prv_start:]
            res.append(TextNode(last_segment, node.text_type))

    return res
