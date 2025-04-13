import unittest

from blocks import (
    markdown_to_blocks,
    block_to_block_type,
    BlockType
)

class TestMarkdownBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
    )
        
    def test_markdown_to_blocks2(self):
        md = """
This is a block. 

This is another block.



This is the last block.
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is a block.",
                "This is another block.",
                "This is the last block."
            ]
        )

    def test_markdown_to_block_empty(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_block_to_block_type_headings(self):
        md = """
#### This is a heading
"""
        block = markdown_to_blocks(md)[0]
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.HEADING, block_type)

    def test_block_to_block_type_headings2(self):
        md = """
######## This is not a heading. It should match para
"""
        block = markdown_to_blocks(md)[0]
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.PARA, block_type)

    def test_block_to_block_type_code(self):
        md = """
```# This is a code block
print(something);
```
"""
        block = markdown_to_blocks(md)[0]
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.CODE, block_type)

    def test_block_to_block_type_code2(self):
        md = """
``# This is NOT a code block
print(something);
``
"""
        block = markdown_to_blocks(md)[0]
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.PARA, block_type)

    def test_block_to_block_type_code3(self):
        md = """
```# This is also NOT a code block
print(something);
`
"""
        block = markdown_to_blocks(md)[0]
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.PARA, block_type)

    def test_block_to_block_type_quote(self):
        md = """
> This is a quote block
> Every line is a quote
> Even this.
"""
        block = markdown_to_blocks(md)[0]
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.QUOTE, block_type)

    def test_block_to_block_type_quote2(self):
        md = """
> This is NOT a quote block
-  Every line is NOT a quote
> Even this.
"""
        block = markdown_to_blocks(md)[0]
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.PARA, block_type)

    def test_block_to_block_type_uol(self):
        md = """
- This is a un-ordered list block
- Every line is a list item
-     Even this.
"""
        block = markdown_to_blocks(md)[0]
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.UOL, block_type)

    def test_block_to_block_type_uol2(self):
        md = """
- This is NOT a un-ordered list block
- Every line is NOT a list item
-this one is culprit.
"""
        block = markdown_to_blocks(md)[0]
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.PARA, block_type)

    def test_block_to_block_type_ol(self):
        md = """
1. something
2. else
3. yes
4. this is an ordered list
"""
        block = markdown_to_blocks(md)[0]
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.OL, block_type)
    
    def test_block_to_block_type_ol2(self):
        md = """
1. something
2. else
36. this line should fail
4. this is NOT an ordered list
"""
        block = markdown_to_blocks(md)[0]
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.PARA, block_type)