import unittest
from blocktypes import BlockType,markdown_to_blocks, block_to_block_type

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
        block = '```This is a code block```'
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

if __name__ == "__main__":
    unittest.main()