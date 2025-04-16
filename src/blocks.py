from enum import Enum
from htmlnode import (
    LeafNode,
    ParentNode,
    text_node_to_html_node
)
from textnode import TextNode, TextType
from conversions import text_to_textnodes
import re

class BlockType(Enum):
    PARA = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UOL = "unordered_list"
    OL = "ordered_list"

def markdown_to_blocks(markdown):
    blocks = markdown.split('\n\n')
    blocks = list(
        filter(
            lambda block: block != "",
            map(lambda block: block.strip(), blocks)
        )
    )
    return blocks

def block_to_block_type(md_block):
    if re.match(r"^#{1,6} ", md_block):
        return BlockType.HEADING
    if len(md_block) >=6 and md_block[:3] == "```" and md_block[-3:] == "```":
        return BlockType.CODE
    
    lines = md_block.splitlines()
    
    if block_lines_start(lines, ">"):
        return BlockType.QUOTE
    if block_lines_start(lines, "- "):
        return BlockType.UOL
    if check_ordered_list(lines):
        return BlockType.OL
    return BlockType.PARA
    

def block_lines_start(md_block_lines, prefix):
    for line in md_block_lines:
        if not line.startswith(prefix):
            return False
    return True

def check_ordered_list(md_block_lines):
    for i in range(len(md_block_lines)):
        if not md_block_lines[i].startswith(f"{i+1}. "):
            return False
    return True

def markdown_to_html_node(markdown):
    children = []
    md_blocks = markdown_to_blocks(markdown)
    for block in md_blocks:
        match block_to_block_type(block):
            case BlockType.PARA:
                lines = block.split("\n")
                paragraph = " ".join(lines)
                child_node = get_children_non_list(paragraph)
                children.append(ParentNode("p", child_node))
            case BlockType.CODE:
                code_block = TextNode(text=block[3:-3].lstrip(), text_type=TextType.CODE)
                children.append(ParentNode("pre", [text_node_to_html_node(code_block)]))
            case BlockType.QUOTE:
                lines = block.split("\n")
                lines = list(map(lambda quote: quote.removeprefix("> "), lines))
                paragraph = " ".join(lines)
                child_node = get_children_non_list(paragraph)
                children.append(ParentNode("blockquote", child_node))
            case BlockType.UOL:
                # Each child must be enclosed in <li> tags
                child_node = get_children_list(block, BlockType.UOL)
                children.append(ParentNode("ul", child_node))
            case BlockType.OL:
                # Each child must be enclosed in <li> tags
                child_node = get_children_list(block, BlockType.OL)
                children.append(ParentNode("ol", child_node))
            case BlockType.HEADING:
                (heading_type, block) = check_heading_type(block)
                child_node = get_children_non_list(block)
                children.append(ParentNode(heading_type, child_node))
    return ParentNode("div", children)

def get_children_non_list(block):
    child_node = []
    text_nodes = text_to_textnodes(block)
    for text_node in text_nodes:
        leaf_node = text_node_to_html_node(text_node)
        child_node.append(leaf_node)
    return child_node

def get_children_list(block, block_type):
    child_node = []
    list_items = block.split("\n")
    i = 1
    for item in list_items:
        if block_type == BlockType.UOL:
            item = item.removeprefix("- ")
        else:
            item = item.removeprefix(f"{i}. ")
        if item.strip() != "":
            child_node.append(ParentNode("li", get_children_non_list(item.strip())))
            i += 1
    return child_node

def check_heading_type(block):
    head_start = re.findall(r"^(#+ )", block)[0]
    return (f"h{len(head_start)-1}", block.removeprefix(head_start))