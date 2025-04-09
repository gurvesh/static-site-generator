from textnode import TextNode, TextType
import re

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
                elif (i & 1 == 0):
                    out.append(TextNode(text_parts[i], TextType.TEXT))
                else:
                    out.append(TextNode(text_parts[i], text_type))
    return out

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)

def split_nodes_image(old_nodes):
    out = []
    for old_node in old_nodes:
        text = old_node.text
        matches = extract_markdown_images(text)
        if matches == []:
            out.append(old_node)
        else:
            for (alt_text, url) in matches:
                sections = text.split(f"![{alt_text}]({url})", 1)
                if sections[0] != "":
                    out.append(TextNode(sections[0], TextType.TEXT))
                out.append(TextNode(alt_text, TextType.IMAGE, url))
                text = sections[1]
        if text != "":
            out.append(TextNode(text, TextType.TEXT))
    return out

def split_nodes_link(old_nodes):
    out = []
    for old_node in old_nodes:
        text = old_node.text
        matches = extract_markdown_links(text)
        if matches == []:
            out.append(old_node)
        else:
            for (alt_text, url) in matches:
                sections = text.split(f"[{alt_text}]({url})", 1)
                if sections[0] != "":
                    out.append(TextNode(sections[0], TextType.TEXT))
                out.append(TextNode(alt_text, TextType.LINK, url))
                text = sections[1]
        if text != "":
            out.append(TextNode(text, TextType.TEXT))
    return out