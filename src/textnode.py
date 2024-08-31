from leafnode import LeafNode


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
