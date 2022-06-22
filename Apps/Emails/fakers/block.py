from Emails.factories.block import BlockFactory


class BlockTestFaker(BlockFactory):
    title: str = "test"
    content: str = "test"
    show_link: bool = True
    link_text: str = "test"
    link: str = "test.com"
