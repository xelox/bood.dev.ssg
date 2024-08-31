from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, children=None, props=None):
        super().__init__(tag, value, children, props)

    def to_html(self):
        if self.children:
            raise ValueError('LeafNode can not have children. sadge')
        if not self.value:
            raise ValueError('value is required on LeafNode.')

        return f"<{self.tag}{super().props_to_html()}>{self.value}</{self.tag}>"

