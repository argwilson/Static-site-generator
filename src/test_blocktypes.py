import unittest
from blocktypes import BlockType,markdown_to_blocks, block_to_block_type, markdown_to_html_node, extract_title

class TestSplitDelimiter(unittest.TestCase):
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
    def test_markdown_to_blocks_two(self):
        md = """
        # This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item
            """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                '# This is a heading',
                'This is a paragraph of text. It has some **bold** and _italic_ words inside of it.',
                '- This is the first list item in a list block\n- This is a list item\n- This is another list item'
            ]
        )

    def test_block_to_blocktype_heading(self):
        block = '### This is a heading'
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_block_to_blocktype_code(self):
        block = '```\nThis is a code block\n```'
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.CODE)

    def test_block_to_blocktype_quote(self):
        block = '>This is a quote\n>This is another quote\n>This is a third quote'
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_block_to_blocktype_unordered(self):
        block = '- This is the first list item in a list block\n- This is a list item\n- This is another list item'
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)

    def test_block_to_blocktype_ordered(self):
        block = '1. This is the first list item in a list block\n2. This is a list item\n3. This is another list item'
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)
    
    def test_block_to_blocktype_paragraph(self):
        block = 'This is a paragraph'
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)
    
    def test_heading(self):
        md = "#### This is a heading"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h4>This is a heading</h4></div>"
        )
    
    def test_quote(self):
        md = """
>This is a quote
>This is another quote
>This is a third quote
            """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote</blockquote><blockquote>This is another quote</blockquote><blockquote>This is a third quote</blockquote></div>"
        )
    
    def test_ordered_list(self):
        md = """
1. This is the first list item in a list block
2. This is a list item
3. This is another list item
        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>This is the first list item in a list block</li><li>This is a list item</li><li>This is another list item</li></ol></div>"
        )
    
    def test_unordered_list(self):
        md = """
- This is the first list item in a list block
- This is a list item
- This is another list item
        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is the first list item in a list block</li><li>This is a list item</li><li>This is another list item</li></ul></div>"
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
    
    def test_extract_title(self):
        md = "# Hello    "
        text = extract_title(md)
        self.assertEqual(text, "Hello")
    
    def test_extract_title_two(self):
        md = "## Hello    "
        with self.assertRaises(Exception):
            extract_title(md)

if __name__ == "__main__":
    unittest.main()