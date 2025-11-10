import unittest

from extractLinks import *
from textnode import *
from delimiter import *
from converter import *


class TestSplit(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_link(self):
        node = TextNode(
            "This is text with a [big ole link](https://biglink.net) and a second [beeeg link](https://beeglink.org)",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("big ole link", TextType.LINK, "https://biglink.net"),
                TextNode(" and a second ", TextType.TEXT),
                TextNode("beeeg link", TextType.LINK, "https://beeglink.org")
            ],
            new_nodes,
        )

    def test_split_link_no_link(self):
        node = TextNode(
            "This is text with no links", TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with no links", TextType.TEXT)
            ],
            new_nodes,
        )

    def test_split_image_no_image(self):
        node = TextNode(
            "This is image with no images", TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is image with no images", TextType.TEXT)
            ],
            new_nodes,
        )
    
    def test_split_image_ending_text(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) more ending texttttt",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" more ending texttttt", TextType.TEXT)
            ],
            new_nodes,
        )

    def test_split_link_ending_text(self):
        node = TextNode(
            "This is text with a [big ole link](https://biglink.net) and a second [beeeg link](https://beeglink.org) dope text",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("big ole link", TextType.LINK, "https://biglink.net"),
                TextNode(" and a second ", TextType.TEXT),
                TextNode("beeeg link", TextType.LINK, "https://beeglink.org"),
                TextNode(" dope text", TextType.TEXT)
            ],
            new_nodes,
        )     

    def test_split_link_no_beginning_text(self):
        node = TextNode(
            "[big ole link](https://biglink.net) and a second [beeeg link](https://beeglink.org) dope text",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("big ole link", TextType.LINK, "https://biglink.net"),
                TextNode(" and a second ", TextType.TEXT),
                TextNode("beeeg link", TextType.LINK, "https://beeglink.org"),
                TextNode(" dope text", TextType.TEXT)
            ],
            new_nodes,
        )     


    def test_split_image_no_beginning_text(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) more ending texttttt",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" more ending texttttt", TextType.TEXT)
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        node = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(node)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes,
        )

    def test_text_to_textnodes_2(self):
        node = "This some `codeeee` and a ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) with _italiccccc_ words and also a [link](https://boot.dev) with some **boldddddd** text!"
        new_nodes = text_to_textnodes(node)
        self.assertListEqual(
            [
                TextNode("This some ", TextType.TEXT),
                TextNode("codeeee", TextType.CODE),
                TextNode(" and a ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" with ", TextType.TEXT),
                TextNode("italiccccc", TextType.ITALIC),
                TextNode(" words and also a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" with some ", TextType.TEXT),
                TextNode("boldddddd", TextType.BOLD),
                TextNode(" text!", TextType.TEXT),
            ],
            new_nodes,
        )