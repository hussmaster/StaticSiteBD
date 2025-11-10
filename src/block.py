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
    #TODO
    #Split the string on newline to check each line
    #Implement count for ordered list to make sure it's in order 1 > 2 > 3 etc
    headings = ["# ", "## ", "### ", "#### ", "##### ", "###### "]
    splitted = markdown.split("\n")
    count = 1
    for split in splitted:
        print(split)
        if split.startswith(">"):
            return BlockType.QUOTE
        elif split.startswith("```") and markdown.endswith("```"):
            return BlockType.CODE
        elif split.startswith("- "):
            return BlockType.UNORDERED_LIST
        elif re.match(rf"{count}+\. ", split):
            print(split)
            print('made it')
            count += 1
            return BlockType.ORDERED_LIST
        elif split.startswith(tuple(headings)):
            return BlockType.HEADING
        else:
            return BlockType.PARAGRAPH