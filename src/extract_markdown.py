import re

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        node_text = old_node.text
        splits = extract_markdown_images(node_text)
        if splits is []:
            return old_node
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