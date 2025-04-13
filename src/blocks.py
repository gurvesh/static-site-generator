from enum import Enum
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
            map(str.strip, blocks)
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