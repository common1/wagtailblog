from django.db import models

from wagtail.models import Page, Orderable
from wagtail.admin.panels import (
    TitleFieldPanel,
    HelpPanel,
    FieldPanel,
    MultiFieldPanel,
    InlinePanel,
    PageChooserPanel,
    FieldRowPanel,
    MultipleChooserPanel,
)
from wagtail.fields import RichTextField
from wagtail.images import get_image_model
from wagtail.documents import get_document_model
from django.core.exceptions import ValidationError

from modelcluster.fields import ParentalKey

class HomePageGalleryImage(Orderable):
    page = ParentalKey('home.HomePage', on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(
        get_image_model(), # 'wagtailimages.Image' can be used as a string
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='+'
    )

class HomePage(Page):
    template = "home/home_page.html"
    max_count = 1
    
    subtitle = models.CharField(max_length=100, blank=True, null=True)
    body = RichTextField(blank=True)
    
     
    custom_document = models.ForeignKey(
        get_document_model(), # 'wagtaildocs.Document'can be used as a string
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    
    cta_url = models.ForeignKey(
        'wagtailcore.Page',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    cta_external_url = models.URLField(blank=True, null=True)

    content_panels = Page.content_panels + [

        # TitleFieldPanel(
        #     'subtitle',
        #     help_text="This is the subtitle that appears below the title on the homepage.",
        #     placeholder="Enter your subtitle",
        # ),
        # InlinePanel(
        #     'gallery_images',
        #     label="Gallery Images",
        #     help_text="Add images to the homepage gallery.",
        #     min_num=2,
        #     max_num=4,
        # )
        
        MultipleChooserPanel(
            'gallery_images',
            label="Gallery Images",
            help_text="Add images to the homepage gallery.",
            max_num=4,
            chooser_field_name='image',
        )
        
        # HelpPanel(
        #     heading="Note:",
        #     content="<strong>Help Panel</strong><p>Help text goes here</p>",
        # ),
        # PageChooserPanel(
        #     'cta_url',
        #     'blogpages.BlogDetail',
        #     help_text="Select the appropriate blog page",
        #     heading="Blog Page Selection",
        # ),
        # FieldRowPanel(
        #     [
        #         PageChooserPanel(
        #             'cta_url',
        #             'blogpages.BlogDetail',
        #             help_text="Select the appropriate blog page",
        #             heading="Blog Page Selection",
        #         ),
        #         FieldPanel(
        #             'cta_external_url',
        #             help_text="Enter the external URL",
        #             heading="External URL",
        #         ),
        #     ],
        #     help_text="Select a page or enter a URL",
        #     heading="Call to Action URLs",
        # ),        
        # MultiFieldPanel(
        #     [
        #         FieldPanel('subtitle'),
        #     ],
        #     heading="MultiFieldPanel demo",
        #     classname="collapsed",
        #     help_text="Random help text",
        # )
        # FieldPanel('subtitle', read_only=True), 
        # FieldPanel('cta_url'), 
        # FieldPanel('cta_external_url'), 
        # FieldPanel('body'),
        # FieldPanel('image'),
        # FieldPanel('custom_document'),
    ]

    @property
    def get_cta_url(self):
        if self.cta_url:
            return self.cta_url.url
        elif self.cta_external_url:
            return self.cta_external_url
        else:
            return None

    def clean(self):
        super().clean()
        
        if self.cta_url and self.cta_external_url:
            raise ValidationError({
                'cta_url': 'You only can have one cta_url',
                'cta_external_url': 'You only can have one cta_url',
            })