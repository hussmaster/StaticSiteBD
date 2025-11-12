from htmlnode import *
from converter import *
from block import *


def markdown_to_html_node(markdown):
    #Split markdown into blocks
    blocks = markdown_to_blocks(markdown)
    childrenNodeList = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.QUOTE:
            html_node = quote_to_html_node(block)
            childrenNodeList.append(html_node)
        elif block_type == BlockType.UNORDERED_LIST:
            containerNode = unordered_to_html_node(block)
            childrenNodeList.append(containerNode)
        elif block_type == BlockType.ORDERED_LIST:
            containerNode = ordered_to_html_node(block)
            childrenNodeList.append(containerNode)
        elif block_type == BlockType.CODE:
            containerNode = code_to_html_node(block)
            childrenNodeList.append(containerNode)
        elif block_type == BlockType.PARAGRAPH:
            block = block.lstrip()
            if block != "":
                containerNode = paragraph_to_html_node(block)
                childrenNodeList.append(containerNode)
        elif block_type == BlockType.HEADING:
            containerNode = heading_to_html_node(block)
            childrenNodeList.append(containerNode)
    masterNode = ParentNode(tag="div",
                          children=childrenNodeList)
    return masterNode
        
#Creates 
def text_to_children(text):
    #Use text_to_textnodes
    #Then use text_node_to_html_node to create child htmlnodes from block_text
    nodes = text_to_textnodes(text)
    children = []
    for node in nodes:
        children.append(text_node_to_html_node(node))
    return children



def quote_to_html_node(block):
    #Splits lines at new line
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        #Strips > from the left side
        new_lines.append(line.lstrip(">").strip())
    #Rejoins lines at spaces
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)
        

def heading_to_html_node(block):
    #Sets first level
    level = 0
    for char in block:
        #Verifies the current character is a #
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    #Gets text of block with index of level + 1
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def unordered_to_html_node(block):
    #Splits at new line
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        #Grab text after "- "
        text = line[2:]
        #send text to text to children function to check for bold, italic etc
        children = text_to_children(text)
        #Create ParentNode
        new_lines.append(ParentNode("li", children))
    #Wrap created child nodes inside of parent nodes
    return ParentNode("ul", new_lines)

def ordered_to_html_node(block):
    #Split lines at new line
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        #Grab text after "#. "
        text = line[3:]
        #Send text to text to children function to check for bold, italic etc
        children = text_to_children(text)
        #Create parentnode 
        new_lines.append(ParentNode("li", children))
    return ParentNode("ol", new_lines)

def paragraph_to_html_node(block):
    #Split lines at new line
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if len(line.strip()) > 0:
            #Make sure it's not an empty string, this is done before getting passed
            #But doing it again
            new_lines.append(line.strip())
    #Rejoin lines with spaces
    content = " ".join(new_lines)
    #Create child text nodes
    children = text_to_children(content)
    return ParentNode("p", children)

def code_to_html_node(block):
    #Verify the block starts and ends iwth ```
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    #Grab text between ``` ```
    text = block[4:-3]
    #Create a textnode with the text
    raw_text_mode = TextNode(text, TextType.TEXT)
    #Create html node from textNode
    child = text_node_to_html_node(raw_text_mode)
    #Create Parentnode with child node created above
    code = ParentNode("code", [child])
    #return Parent node with previous node nested
    return ParentNode("pre", [code])