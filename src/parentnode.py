from htmlnode import HTMLNode
from leafnode import LeafNode


class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError('No Tag.')
        if not self.children:
            raise ValueError('ParenNode must have children')

        children_str = ""
        for child in self.children:
            if not isinstance(child, LeafNode):
                raise ValueError('Children Of ParentNode must all be LeafNode')
            children_str += child.to_html()

        return f"<{self.tag}{super().props_to_html()}>{children_str}</{self.tag}>"
