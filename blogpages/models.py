from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel

from django.core.exceptions import ValidationError

class BlogIndex(Page):
    # A listing page of all child pages
    
    template = 'blogpages/blog_index_page.html'
    max_count = 1
    parent_page_types = ['home.HomePage']
    subpage_types = ['blogpages.BlogDetail']

    subtitle = models.CharField(max_length=100, blank=True)
    body = RichTextField(blank=True)
    
    content_panels = Page.content_panels + [
        FieldPanel('subtitle'),
        FieldPanel('body'),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context['blogpages'] = BlogDetail.objects.live().public()
        return context



class BlogDetail(Page):   
    parent_page_types = ['blogpages.BlogIndex']
    subpage_types = []

    subtitle = models.CharField(max_length=100, blank=True)
    body = RichTextField(
        blank=True,
        features=['blockquote', 'h3', 'image', 'ul', 'strikethrough', 'code'],
    )
    
    content_panels = Page.content_panels + [
        FieldPanel('subtitle'),
        FieldPanel('body'),
    ]

    def clean(self):
        super().clean()
        
        errors = {}
        
        if 'blog' in self.title.lower():
            errors['title'] = "Title cannot have the word 'blog'"

        if 'blog' in self.subtitle.lower():
            errors['subtitle'] = "Subtitle cannot have the word 'blog'"
        
        if 'blog' in self.slug.lower():
            errors['slug'] = "Slug cannot have the word 'blog'"
        
        if errors:
            raise ValidationError(errors)