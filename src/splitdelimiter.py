from textnode import TextNode, TextType
from extract_markdown import extract_markdown_images, extract_markdown_links

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    delimiters = {TextType.BOLD:'**', TextType.ITALIC:'_', TextType.CODE:'`'}
    if delimiters[text_type] != delimiter:
        raise Exception('Error: text type does not match expected delimiter')
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        node_text = old_node.text
        splits = extract_markdown_links(node_text)
        if splits == []:
            new_nodes.append(old_node)
            continue
        sections = []
        for i in range(len(splits)):
            link_alt, link_url = splits[i]
            text_split = node_text.split(f"[{link_alt}]({link_url})", 1)
            sections.extend([text_split[0], f"[{link_alt}]({link_url})", text_split[1]])
            if extract_markdown_links(text_split[1]) != []:
                node_text = sections.pop()
        split_nodes = []
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                j = int((i-1)/2)
                link_alt, link_url = splits[j]
                split_nodes.append(TextNode(link_alt, TextType.LINK, link_url))
        new_nodes.extend(split_nodes)
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        node_text = old_node.text
        splits = extract_markdown_images(node_text)
        if splits == []:
            new_nodes.append(old_node)
            continue
        sections = []
        for i in range(len(splits)):
            image_alt, image_link = splits[i]
            text_split = node_text.split(f"![{image_alt}]({image_link})", 1)
            sections.extend([text_split[0], f"![{image_alt}]({image_link})", text_split[1]])
            if extract_markdown_images(text_split[1]) != []:
                node_text = sections.pop()
        split_nodes = []
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                j = int((i-1)/2)
                image_alt, image_link = splits[j]
                split_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
        new_nodes.extend(split_nodes)
    return new_nodes

def split_nodes(old_nodes):
    new_nodes = []
    new_nodes = split_nodes_delimiter(old_nodes, '**', TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, '_', TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, '`', TextType.CODE)
    new_nodes = split_nodes_link(new_nodes)
    new_nodes = split_nodes_image(new_nodes)
    return new_nodes