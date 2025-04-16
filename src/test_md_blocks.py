import unittest

from blocks import (
    markdown_to_blocks,
    block_to_block_type,
    BlockType,
    markdown_to_html_node
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
    
    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_unordered_list(self):
        md = """
- This is a un-ordered **list** block
- Every line is a list item
-        Even this.
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><ul><li>This is a un-ordered <b>list</b> block</li><li>Every line is a list item</li><li>Even this.</li></ul></div>'
        )
    
    def test_ordered_list(self):
        md = """
1. something
2. else
3. yes
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><ol><li>something</li><li>else</li><li>yes</li></ol></div>'
        )

    def test_heading(self):
        md = "##### This is a heading **with bold** and _italics_"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><h5>This is a heading <b>with bold</b> and <i>italics</i></h5></div>'
        )

    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and _more_ items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

    def test_code(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

if __name__ == "__main__":
    unittest.main()