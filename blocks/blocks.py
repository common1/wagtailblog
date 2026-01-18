from django.core.exceptions import ValidationError
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock

class TextBlock(blocks.TextBlock):
    
    def __init__(self, **kwargs):
        super().__init__(
            **kwargs,
            help_text = "This is from my TextBlock (help text is here)",
            max_length=10,
            min_length=2,
            required=False,
        )        

    def clean(self, value):
        value = super().clean(value)
        
        if "wordpress" in value.lower():
            raise ValidationError("The word 'wordpress' is not allowed.")

        return value

    class Meta:
        template = "blocks/text_block.html"
        icon = "strikethrough"
        group = "Standalone blocks"

class InfoBlock(blocks.StaticBlock):
    
    class Meta:
        # icon = "..."
        group = ""
        template = "blocks/info_block.html"
        admin_text = "This is my InfoBlock"
        label = "General Information"
        group = "Standalone blocks"

from wagtail.blocks import StructBlockValidationError, ListBlockValidationError

class FAQBlock(blocks.StructBlock):
    question = blocks.CharBlock()
    answer = blocks.RichTextBlock(
        features = ['bold', 'italic',]
    )

    # def clean(self, value):
    #     cleaned_data = super().clean(value)
    #     if 'wordpress' in str(cleaned_data['answer']).lower():
    #         raise StructBlockValidationError(
    #             block_errors={
    #                 'answer': ValidationError("We don't like WordPress here!")
    #             }
    #         )
    #     return cleaned_data

class FAQListBlock(blocks.ListBlock):
    def __init__(self, **kwargs):
        super().__init__(FAQBlock(), **kwargs)
        
    def clean(self, value):
        cleaned_data = super().clean(value)
        errors = {}

        for index, obj in enumerate(cleaned_data):
            if 'wordpres' in str(obj['answer']).lower():
                errors[index] = ValidationError("We don't like WordPress here!")

        if errors:
            raise ListBlockValidationError(block_errors=errors)

        return cleaned_data

    class Meta:
        min_num = 1
        max_num = 5
        label = "Frequently Asked Questions"
        # icon = "..."
        template = "blocks/faq_list_block.html"
        group = "Iterables"


class CarouselBlock(blocks.StreamBlock):
    image = ImageChooserBlock()
    quotation = blocks.StructBlock(
        [
            ('text', blocks.TextBlock()),
            ('author', blocks.TextBlock()),
        ]
    )
    
    def clean(self, value):
        images = [item for item in value if item.block_type == 'image']
        quotations = [item for item in value if item.block_type == 'quotation']

        if not images or not quotations:
            raise ValidationError("You must have at least one image and one quotations")

        if len(images) != len(quotations):
            raise ValidationError("You must have the same number of images and quotations")
        return super().clean(value)

    class Meta:
        template = "blocks/carousel_block.html"
        group = "Iterables"


class CallToAction1(blocks.StructBlock):
    text = blocks.RichTextBlock(
        features=['bold', 'italic'],
        required=True,
    )
    page = blocks.PageChooserBlock()
    button_text = blocks.CharBlock(
        max_length=100,
        required= False,
    )

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        page = value.get('page')
        button_text = value.get('button_text')
        context['button_copy'] = button_text if button_text else f'Read: {page.title}'

        return context

    class Meta:
        label="CTA #1"
        template = "blocks/call_to_action_1.html"

class ImageBlock(ImageChooserBlock):

    def get_context(self, value, parent_context=None):
        from blogpages.models import BlogDetail
        context = super().get_context(value, parent_context=parent_context)
        context['blog_posts'] = BlogDetail.objects.all().live().public()
        return context

    class Meta:
        template = "blocks/image_block.html"
        group = "Standalone blocks"

