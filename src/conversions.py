from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    out = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            out.append(old_node)
        else:
            text = old_node.text
            text_parts = text.split(delimiter)
            n_parts = len(text_parts)
            if (n_parts & 1) != 1: # We have an odd number of parts, which means closing delimiter was missing
                raise Exception(f"matching delimiter not found in {old_node} of type {delimiter}")
            for i in range(n_parts):
                if text_parts[i] == "":
                    continue
                if (i & 1 == 0):
                    out.append(TextNode(text_parts[i], TextType.TEXT))
                else:
                    out.append(TextNode(text_parts[i], text_type))
    return out