
class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
        pass

    def __repr__(self):
        return f"\nHTMLNode(\n    {self.tag},\n    {self.value},\n    {self.children},\n    {self.props}\n)\n"

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if not self.props:
            return ""

        return ''.join(map(lambda kv: f" {kv[0]}=\"{kv[1]}\"", self.props.items()))

