class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
    def to_html(self):
        # Converts node to html format (will work for inherited subclasses)
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self):
        # If a HTMLNode (or associated node) has a prop, it converts it to a html string.
        if self.props is None:
            return ""
        key_string = ''
        for key in self.props.keys():
            key_string += f' {key}="{self.props[key]}"'
        return key_string

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        # Converts node to html format
        if self.value is None:
            raise ValueError("invalid HTML: no value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        # Converts node to html format
        if self.tag is None:
            raise ValueError("invalid HTML: no tag")
        if self.children is None:
            raise ValueError("invalid HTML: no children")
        return f"<{self.tag}{self.props_to_html()}>{''.join([child.to_html() for child in self.children])}</{self.tag}>"
    
    def __repr__(self):
        return f"ParentNode({self.tag}, {[repr(child) for child in self.children]}, {self.props})"