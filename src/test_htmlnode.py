import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType
from converter import text_node_to_html_node
from delimiter import split_nodes_delimiter, split_nodes_image, split_nodes_link
from extractLinks import extract_markdown_images, extract_markdown_links


class TestHtmlNode(unittest.TestCase):
    def test_eq(self):
        testEQProps = {
            "href": "https://www.google.com",
            "target": "_blank"
        }
        final = ' href="https://www.google.com" target="_blank"'
        node = HTMLNode("p", "p value", props=testEQProps)
        convert = node.props_to_html()
        self.assertEqual(convert, final)

    def test_uneq(self):
        testEQProps = {
            "href": "https://www.google.com",
            "target": "_blank"
        }
        final = 'href="https://www.google.com" target="_blank"'
        node = HTMLNode("p", "p value", props=testEQProps)
        convert = node.props_to_html()
        self.assertNotEqual(convert, final)

    def test_eq2(self):
        testEQProp = {
            "poggers": "poggers.com",
            "lockon": "true_"
        }
        final = ' poggers="poggers.com" lockon="true_"'
        node = HTMLNode("a", "a value", props=testEQProp)
        convert = node.props_to_html()
        self.assertEqual(convert, final)

    def test_p(self):
        node = LeafNode("p", "some paragraphs")
        convert = node.to_html()
        self.assertEqual(convert, "<p>some paragraphs</p>")

    def test_LF(self):
        testEQProp = {
            "href": "poggers.com",
            "lockon": "true_"
        }
        node = LeafNode("a", "click this!", props=testEQProp)
        convert = node.to_html()
        self.assertEqual(convert, '<a href="poggers.com" lockon="true_">click this!</a>')

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    def test_to_html_with_multiple_children(self):
        lfNode3 = LeafNode("i", "italic text")
        lfNode4 = LeafNode("b", "bold text")
        parent_node = ParentNode("span", [lfNode3, lfNode4])
        self.assertEqual(
            parent_node.to_html(),
            "<span><i>italic text</i><b>bold text</b></span>"
        )

    def test_to_html_with_multiple_children_grandchildren(self):
        lfNode3 = LeafNode("i", "italic text")
        lfNode4 = LeafNode("b", "bold text")
        parent_node1 = ParentNode("div", [lfNode3])
        parent_node2 = ParentNode("span", [parent_node1, lfNode4])
        self.assertEqual(
            parent_node2.to_html(),
            "<span><div><i>italic text</i></div><b>bold text</b></span>"
        )
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")


    def test_image(self):
        node = TextNode("An orc", TextType.IMAGE, url="https://img/ork.png")
        html = text_node_to_html_node(node)
        self.assertEqual(html.tag, "img")
        self.assertEqual(html.value, "")
        self.assertEqual(html.props, {"src": "https://img/ork.png", "alt": "An orc"})

    def test_link(self):
        node = TextNode("Click here", TextType.LINK, url="https://test.com")
        html = text_node_to_html_node(node)
        self.assertEqual(html.tag, "a")
        self.assertEqual(html.value, "Click here")
        self.assertEqual(html.props, {"href": "https://test.com"})

    def test_bold(self):
        node = TextNode("big bold text", TextType.BOLD)
        html = text_node_to_html_node(node)
        self.assertEqual(html.tag, "b")
        self.assertEqual(html.value, "big bold text")

    def test_link_error(self):
        node = TextNode("url text", TextType.LINK)
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

    def test_image_error(self):
        node = TextNode("image error", TextType.IMAGE)
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

    def test_invalid_error(self):
        node = TextNode("generic", "FakeType")
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_markdown_links(self):
        matches = extract_markdown_links("This is text with a link [to jomama](https://test.com) and [to floatplane](https://www.floatplane.com)")
        self.assertListEqual([("to jomama", "https://test.com"), ("to floatplane", "https://www.floatplane.com")], matches)
