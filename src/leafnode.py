from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.value:
            raise ValueError('value is required on LeafNode.')

        return f"<{self.tag}{super().props_to_html()}>{self.value}</{self.tag}>"

