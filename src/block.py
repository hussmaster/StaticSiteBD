from enum import Enum
import re

#Class for specific block types
class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

#Takes a single block of markdown text as input and returns the blocktype enum
def block_to_block_type(markdown):
    split = markdown.split("\n")
    if markdown.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(split) > 1 and split[0].startswith("```") and split[-1].startswith("```"):
        return BlockType.CODE
    if markdown.startswith(">"):
        for s in split:
            if not s.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if markdown.startswith("- "):
        for s in split:
            if not s.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    if markdown.startswith("1. "):
        count = 1
        for s in split:
            if not s.startswith(f"{count}. "):
                return BlockType.PARAGRAPH
            count += 1
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH