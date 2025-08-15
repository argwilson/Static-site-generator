from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    if not isinstance(old_nodes, list):
        raise Exception("Error: Expecting a list of nodes.")
    delimiters = {TextType.BOLD:'**', TextType.ITALIC:'_', TextType.CODE:'`'}
    if delimiters[text_type] != delimiter:
        raise Exception('Error: text type does not match expected delimiter')
    node_list = []
    for node in old_nodes:
        text_list = node.text.split(delimiter)
        new_nodes = [
            TextNode(text=text_list[0], text_type=TextType.TEXT),
            TextNode(text=text_list[1], text_type=text_type),
            TextNode(text=text_list[2], text_type=TextType.TEXT)
        ]
        node_list.append(new_nodes)
    if len(old_nodes) == 1:
        return node_list[0]
    return node_list
        

        

        
