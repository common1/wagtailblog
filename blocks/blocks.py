from wagtail import blocks

class TextBlock(blocks.TextBlock):
    
    def __init__(self, **kwargs):
        super().__init__(
            **kwargs,
            help_text = "This is from my TextBlock (help text is here)"
        )        

    class Meta:
        # template = "..."
        ...

class InfoBlock(blocks.StaticBlock):
    
    class Meta:
        # icon = "..."
        # template = "..."
        admin_text = "This is my InfoBlock"
        label = "General Information"

class FAQBlock(blocks.StructBlock):
    question = blocks.CharBlock()
    answer = blocks.RichTextBlock(
        features = ['bold', 'italic',]
    )

class FAQListBlock(blocks.ListBlock):
    def __init__(self, **kwargs):
        super().__init__(FAQBlock(), **kwargs)
        
    class Meta:
        min_num = 1
        max_num = 5
        label = "Frequently Asked Questions 2"
        # icon = "..."
        # template = "..."

