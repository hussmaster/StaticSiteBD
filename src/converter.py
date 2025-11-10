from textnode import TextType
from htmlnode import LeafNode
from delimiter import *
from extractLinks import *

#Converts text_type to a new LeafNode with proper TextType enum
def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK:
        if not text_node.url:
            raise ValueError("Link requires a url")
        else:
            return LeafNode("a", text_node.text, props={"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        if not text_node.url:
            raise ValueError("Image requires a url")
        else:
            return LeafNode("img", "", props={"src": text_node.url,
                                            "alt": text_node.text})
    else:
        raise ValueError("Text Type isn't a valid type")
    


#Convert raw string of markdown into a list of TextNode objects
def text_to_textnodes(text):
    #Create the beginning TextNode with all the text as a Text Type of Text
    nodes = [TextNode(text, TextType.TEXT)]
    #Chain through bold > Italic > Code > images > links
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

#Takes raw markdown string and returns a list of "block" strings
def markdown_to_blocks(markdown):
    #Splits on double newline
    text = markdown.split("\n\n")
    returnText = []
    for t in text:
        #Strips each index of leading or trailing whitespace
        returnText.append(t.strip("\n"))
    return returnText