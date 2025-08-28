from enum import Enum
from htmlnode import ParentNode
from textnode import TextNode, TextType, text_node_to_html_node
from splitdelimiter import split_nodes

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

def text_to_child_node(text):
    text_node = TextNode(text, TextType.TEXT)
    text_nodes = split_nodes([text_node])
    child_nodes = []
    for node in text_nodes:
        new_node = text_node_to_html_node(node)
        child_nodes.append(new_node)
    return child_nodes

def heading_to_node(block):
    heading_list = block.split(" ", 1)
    heading_value = len(heading_list[0])
    child_nodes = text_to_child_node(heading_list[1])
    return [ParentNode(f"h{heading_value}", child_nodes)]

def quote_to_nodes(block):
    new_blocks = block.split("\n")
    new_lines = []
    for new_block in new_blocks:
        if not new_block.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(new_block.lstrip(">").strip())
    content = " ".join(new_lines)
    child_nodes = text_to_child_node(content)
    return [ParentNode("blockquote", child_nodes)]

def ol_to_nodes(block):
    lines = block.split("\n")
    i = 1
    line_nodes = []
    for line in lines:
        line = line.replace(f"{i}. ", "")
        child_nodes = text_to_child_node(line)
        line_nodes.append(ParentNode("li", child_nodes))
        i += 1
    return [ParentNode("ol", line_nodes)]

def ul_to_nodes(block):
    lines = block.split("\n")
    line_nodes = []
    for line in lines:
        line = line.replace("- ", "")
        child_nodes = text_to_child_node(line)
        line_nodes.append(ParentNode("li", child_nodes))
    return [ParentNode("ul", line_nodes)]

def code_to_node(block):
    new_block = block.strip("```")
    new_block = new_block.split("\n", 1)[1]
    text_node = TextNode(new_block, TextType.CODE)
    child_node = text_node_to_html_node(text_node)
    return [ParentNode("pre", [child_node])]

def text_to_node(block):
    new_block = block.replace("\n", " ")
    child_nodes = text_to_child_node(new_block)
    return [ParentNode("p", child_nodes)]

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type is BlockType.HEADING:
            nodes.extend(heading_to_node(block))
        elif block_type is BlockType.QUOTE:
            nodes.extend(quote_to_nodes(block))
        elif block_type is BlockType.ORDERED_LIST:
            nodes.extend(ol_to_nodes(block))
        elif block_type is BlockType.UNORDERED_LIST:
            nodes.extend(ul_to_nodes(block))
        elif block_type is BlockType.CODE:
            nodes.extend(code_to_node(block))
        else:
            nodes.extend(text_to_node(block))
    return ParentNode("div", nodes)
    
def extract_title(markdown):
    block = markdown_to_blocks(markdown)[0]
    block_type = block_to_block_type(block)
    if block_type is not BlockType.HEADING:
        raise Exception("Warning, no h1 heading found")
    heading_list = block.split(" ", 1)
    if len(heading_list[0]) != 1:
        raise Exception("Warning, no h1 heading found")
    text = heading_list[1].strip()
    return text