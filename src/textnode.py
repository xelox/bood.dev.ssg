from leafnode import LeafNode
from parentnode import ParentNode
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
            res.append(TextNode(left_seg, node.text_type, node.url))
            alt = item.group(1)
            url = item.group(2)
            res.append(TextNode(alt, link_type, url))
            prv_start = item.end()

        if prv_start != len(node.text):
            last_segment = node.text[prv_start:]
            res.append(TextNode(last_segment, node.text_type, node.url))

    return res

def md_to_textnodes(md: str):
    output = split_delimiter([TextNode(md, 'text')], '**', 'bold')
    output = split_delimiter(output, '*', 'italic')
    output = split_delimiter(output, '`', 'code')
    output = split_link(output, 'image')
    output = split_link(output, 'link')
    return output

def md_to_blocks(md: str):
    res = []
    block = []
    for line in md.split('\n'):
        line = line.strip()
        if line == '':
            if block:
                res.append(block)
            block = []
        else:
            block.append(line)

    if block:
        res.append(block)

    return res

def block_to_block_type(block):
    first_line: str = block[0]
    heading_pattern = r'^#{1,6} .*$'
    if re.match(heading_pattern, first_line):
        return 'heading'

    last_line: str = block[-1]
    if first_line.startswith('```') and last_line.endswith('```'):
        return 'code'

    is_quote = True
    is_ulist = True
    is_olist = True
    for idx, line in enumerate(block):
        if not line.startswith('>'):
            is_quote = False
        if not (line.startswith('- ') or line.startswith('* ')):
            is_ulist = False
        if not line.startswith(f"{idx + 1}. "):
            is_olist = False

    if is_quote:
        return 'quote'
    if is_olist:
        return 'ordered_list'
    if is_ulist:
        return 'unordered_list'

    return 'paragraph'

def md_line_to_html_str(md):
    return ''.join(
        map(lambda html_node: html_node.to_html(),
            map(lambda txtnode: txtnode.to_html_node(), md_to_textnodes(md))))

def md_to_html(md):
    body_children = []
    for block in md_to_blocks(md):
        block_type = block_to_block_type(block)
        match block_type:
            case 'heading':
                line = block[0]
                h_count = len(re.match(r'^#+', line).group(0))
                line.lstrip('#' * h_count + ' ')
                body_children.append(LeafNode(f'h{h_count}', md_line_to_html_str(md)))
            case 'code':
                block[0].lstrip('```')
                block[-1].rstrip('```')
                md = '\n'.join(block)
                code = LeafNode(None, md_line_to_html_str(md))
                pre = ParentNode('pre', children=[code])
                body_children.append(pre)
            case 'quote':
                md = '\n'.join(block)
                quote = LeafNode('blockquote', md_line_to_html_str(md))
                body_children.append(quote)
            case 'unordered_list':
                children = []
                for item in block:
                    leaf = md_line_to_html_str(re.sub(r'- |\* ', '', item))
                    children.append(LeafNode('li', leaf))
                olist = ParentNode('ul', children)
                body_children.append(olist)
            case 'ordered_list':
                children = []
                for item in block:
                    leaf = md_line_to_html_str(re.sub(r'\d+\. ', '', item))
                    children.append(LeafNode('li', leaf))
                olist = ParentNode('ol', children)
                body_children.append(olist)
            case 'paragraph':
                value = md_line_to_html_str('\n'.join(block))
                p = LeafNode('p', value)
                body_children.append(p)


            case _:
                raise ValueError(f'{block_type} block type not implemented')

    return ParentNode('body', body_children).to_html()
