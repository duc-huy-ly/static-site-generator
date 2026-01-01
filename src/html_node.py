class HTMLNode:
    """    
    tag - A string representing the HTML tag name (e.g. "p", "a", "h1", etc.)
    value - A string representing the value of the HTML tag (e.g. the text inside a paragraph)
    children - A list of HTMLNode objects representing the children of this node
    props - A dictionary of key-value pairs representing the attributes of the HTML tag. For example, a link (<a> tag) might have {"href": "https://www.google.com"}
    """
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
        
    # Children will have to implement this
    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props:
            res = []
            for k, v in self.props.items():
                res.append(f'{k}="{v}"')
            return ' '.join(res)
        return ""
    
    def __repr__(self):
        return f"""HTMLNode object:
        tag:{self.tag}
        value:{self.value}
        children:{self.children}
        props:{self.props_to_html()}
        """
        
class LeafNode(HTMLNode):
    def __init__(self,tag, value, props=None):
        super().__init__(tag, value, None, props)
        
    def to_html(self):
        if not self.value:
            raise ValueError("All leaf nodes should have a value")
        if not self.tag:
            return str(self.value)
        if self.props:
            return f"<{self.tag} {self.props_to_html()}>{self.value}</{self.tag}>"
        return f"<{self.tag}>{self.value}</{self.tag}>"