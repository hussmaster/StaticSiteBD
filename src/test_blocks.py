import unittest

from converter import *

class TestSplit(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_2(self):
        md = """
# This is a nice heading

This here be some texttttttt with `code blocks` and  **bold** words

- This is a list item
- This is also a list item

- This is a second list list item
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# This is a nice heading",
                "This here be some texttttttt with `code blocks` and  **bold** words",
                "- This is a list item\n- This is also a list item",
                "- This is a second list list item",
            ],
        )


    