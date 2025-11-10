
#Creating HTMLNode with properties
class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props


    #Function to process props dictionary
    def props_to_html(self):
        if self.props == None:
            return ""
        result = []
        for k,v in self.props.items():
            result.append(f' {k}="{v}"')
        final = "".join(result)
        return final
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


#Child Node, cannot have children
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        #Inherit values from HTMLNode but cannot have children
        super().__init__(tag=tag, value=value, children=None, props=props)
    #Converts values to raw html tag value props to <tag props_to_html>value</tag>
    def to_html(self):
        if self.value is None:
            raise ValueError('No value present')
        elif self.tag is None:
            return self.value
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
#Parent node, must not have a valuebootdev run 4e8c8d2a-8966-4e7d-acdf-067b1d06225f
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        #Inherit values from HTMLNode, cannot have a value
        super().__init__(tag=tag, value=None, children=children, props=props)
    #Converts values to raw html recursively on children
    def to_html(self):
        if self.tag is None:
            raise ValueError('No tag present')
        elif self.children is None:
            raise ValueError('No children present')
        else:
            result = f"<{self.tag}>"
            for i in self.children:
                result += f"{i.to_html()}"
            result += f"</{self.tag}>"
            return result