import re
from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    new_blocks = []
    for block in blocks:
        block = block.strip()
        if block == "":
            continue
        new_blocks.append(block)
    return new_blocks

def block_to_block_type(block):
    if re.findall(r"^#{1,6} .+", block):
        return BlockType.HEADING
    if re.findall(r"^`{3}.+`{3}$", block):
        return BlockType.CODE
    verify_blocks = []
    if re.findall(r"^>.+", block):
        small_block = block.split("\n")
        for small in small_block:
            verify_blocks.append(re.findall(r"^>.+", small) != [])
        if sum(verify_blocks) == len(small_block):
            return BlockType.QUOTE
    if re.findall(r"^- .+", block):
        small_block = block.split("\n")
        for small in small_block:
            verify_blocks.append(re.findall(r"^- .+", small) != [])
        if sum(verify_blocks) == len(small_block):
            return BlockType.UNORDERED_LIST
    if re.findall(r"1\. .+", block):
        small_block = block.split("\n")
        for i in range(len(small_block)):
            verify_blocks.append(re.findall(rf"{i+1}\. .+", small_block[i]) != [])
        if sum(verify_blocks) == len(small_block):
            return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH