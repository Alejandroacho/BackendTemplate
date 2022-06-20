from Emails.factories.block import BlockFactory


class BlockTestFaker(BlockFactory):
    title = 'test'
    content = 'test'
    show_link = True
    link_text = 'test'
    link = 'test.com'
