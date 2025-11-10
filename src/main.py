from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from delimiter import split_nodes_delimiter, split_nodes_link, split_nodes_image
from extractLinks import extract_markdown_images, extract_markdown_links
from converter import *
from block import *

testEQProps = {
    "href": "https://www.google.com",
    "lockon": "true_"
}


def main():
    newNode = TextNode("This is some anchor test", TextType.LINK, "https://boot.dev")
    #print(newNode)
    htNode = HTMLNode("a", "click this!", props=testEQProps)
    #print(htNode)
    method = htNode.props_to_html()
    #print(method)
    lfNode = LeafNode("p", "")
    method3 = lfNode.to_html()
    #print(method3)
    lfNode2 = LeafNode("a", "click this!", props=testEQProps)
    method4 = lfNode2.to_html()
    #print(method4)
    pNode = ParentNode("p", [lfNode2])
    pNode2 = ParentNode("b", [pNode])
    lfNode3 = LeafNode("i", "italic text")
    lfNode4 = LeafNode("b", "bold text")
    method5 = pNode2.to_html()
    #print(method5)
    pNode3 = ParentNode("div", [lfNode3, lfNode4])
    method6 = pNode3.to_html()
    #print(method6)
    pNode4 = ParentNode("div", [])
    method7 = pNode4.to_html()
    #print(method7)


    node = TextNode("This is text with a `code block` word", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
    #print(new_nodes)

    node2 = TextNode("This is a text block", TextType.TEXT)
    new_nodes2 = split_nodes_delimiter([node2], "`", TextType.CODE)
    #print(new_nodes2)

    node3 = TextNode("a **b** c **d** e", TextType.TEXT)
    new_nodes3 = split_nodes_delimiter([node3], "**", TextType.BOLD)
    #print(new_nodes3)

    node4 = TextNode("a **b c** d", TextType.TEXT)
    new_nodes4 = split_nodes_delimiter([node4], "**", TextType.BOLD)
    #print(new_nodes4)

    node5 = TextNode("a **b** c **d**", TextType.TEXT)
    new_nodes5 = split_nodes_delimiter([node5], "**", TextType.BOLD)
    #print(new_nodes5)

    text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg"
    text2 = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
    #print(extract_markdown_images(text))
    #print(extract_markdown_links(text2))
    linkNode = TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg) extra text", TextType.TEXT)
    #print(split_nodes_image([linkNode]))

    #nolinkNode = TextNode("This text with no links at all", TextType.TEXT)
    #print(split_nodes_link([nolinkNode]))
    extraCurrentNode = TextNode("This is text with a link [to jo](https://jo.mama.com) and [to test](https://test.com) extra text", TextType.TEXT)
    #print(split_nodes_link([extraCurrentNode]))

    text3 = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
    #print(text_to_textnodes(text3))

    #text4 = "[a \c`c](url)`"
    #print(text_to_textnodes(text3))

    md = """
# Heading Test

#Heading test

## Heading Test

###### Heading Test

####### Heading test

####### Bad heading test

This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items

1. ordered list
2. ordered list 2

> Quote test

```Some code text```
"""
    blocks = markdown_to_blocks(md)
    print(blocks)
    for block in blocks:
        print(block_to_block_type(block))

if __name__ == "__main__":
    main()