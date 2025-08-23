from enum import Enum
from htmlnode import HTMLNode

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
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type is BlockType.CODE:
            new_block = block.replace("```", "")
            node = HTMLNode(tag="pre", children=HTMLNode(tag="code", value=new_block))
        elif block_type is BlockType.HEADING:
            heading = block.split(" ")[0]
            i = len(heading.split())
            new_block = block.replace(heading, "")
            node = HTMLNode(tag=f"h{i+1}", value=new_block)
        elif block_type is BlockType.QUOTE:
            new_block = block.replace(">", "")
            node = HTMLNode(tag="blockquote", value=new_block)
        elif block_type is BlockType.UNORDERED_LIST:
            lines = block.split("\n")
            nodes = []
            for line in lines:
                new_line = line.replace("- ", "")
                new_node = HTMLNode(tag="li", value=new_line)
                nodes.append(new_node)
            node = HTMLNode(tag="ul", value=nodes)
        elif block_type is BlockType.ORDERED_LIST:
            lines = block.split("\n")
            nodes = []
            i = 1
            for line in lines:
                new_line = line.replace(f"{i}.  ", "")
                i += 1
                new_node = HTMLNode(tag="li", value=new_line)
                nodes.append(new_node)
            node = HTMLNode(tag="ol", value=nodes)