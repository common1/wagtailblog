from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel

from django.core.exceptions import ValidationError

from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.fields import StreamField
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.snippets.blocks import SnippetChooserBlock
from wagtail import blocks

from blocks import blocks as custom_blocks

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

class BlogPageTags(TaggedItemBase):
    content_object = ParentalKey(
        'blogpages.BlogDetail',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )

from django.contrib.contenttypes.fields import GenericRelation
from wagtail.admin.panels import PublishingPanel
from wagtail.models import (
    DraftStateMixin, 
    RevisionMixin, 
    LockableMixin,
    PreviewableMixin,
)

from wagtail.search import index

class Author(
    PreviewableMixin,
    LockableMixin, 
    DraftStateMixin, 
    RevisionMixin,
    index.Indexed,
    models.Model
):
    name = models.CharField(max_length=255)
    bio = models.TextField()
    revisions = GenericRelation("wagtailcore.Revision", related_query_name="author")
       
    panels = [
        FieldPanel('name', permission="blogpages.can_edit_author_name"),
        FieldPanel('bio'),
        PublishingPanel(),
    ]

    search_fields = [
        index.FilterField('name'),
        index.SearchField('name'),
        index.AutocompleteField('name'),
    ]

    def __str__(self):
        return self.name
    
    @property
    def preview_modes(self):
        return PreviewableMixin.DEFAULT_PREVIEW_MODES + [
            ("dark_mode", "Dark Mode"),
        ]
    
    def get_preview_template(self, request, mode_name):
        templates = {
            "": "includes/author.html", # Default
            "dark_mode": "includes/author_dark_mode.html",
        }
        return templates.get(mode_name, templates[""])
    
    def get_preview_context(self, request, mode_name):
        context = super().get_preview_context(request, mode_name)
        if mode_name == "dark_mode":
            context['warning'] = "This is a preview in dark mode"
        return context
    
    class Meta:
        permissions = [
            ("can_edit_author_name", "Can edit author name")
        ]
# 1. ImageChooserBlock
# 2. DocumentChooserBlock
# 3. PageChooserBlock
# 4. SnippetChooserBlock

class BlogDetail(Page):   
    subtitle = models.CharField(max_length=100, blank=True)
    tags = ClusterTaggableManager(through=BlogPageTags, blank=True)
    author = models.ForeignKey(
        'blogpages.Author',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    body = StreamField(
        [
            ('info', custom_blocks.InfoBlock()),
            ('faq', custom_blocks.FAQListBlock()),
            ('text', custom_blocks.TextBlock()),
            ('carousel', custom_blocks.CarouselBlock()),
            ('image', custom_blocks.ImageBlock()),
            ('doc', DocumentChooserBlock(
                group = "Standalone blocks",
            )),
            ('page', blocks.PageChooserBlock(
                required=False,
                page_type='home.HomePage',
                group = "Standalone blocks",
            )),
            ('author', SnippetChooserBlock('blogpages.author')),
            ('call_to_action_1', custom_blocks.CallToAction1()),
        ],
        block_counts={
            # 'text': {'min_num': 1},
            # 'image': {'max_num': 1},
        },
        use_json_field=True,
        blank=True,
        null=True,
    )

    parent_page_types = ['blogpages.BlogIndex']
    subpage_types = []
    
    content_panels = Page.content_panels + [
        FieldPanel('subtitle', read_only=True),
        FieldPanel('body'),
        FieldPanel('tags'),
    ]

    def clean(self):
        super().clean()
        
        errors = {}
        
        # if 'blog' in self.title.lower():
        #     errors['title'] = "Title cannot have the word 'blog'"

        # if 'blog' in self.subtitle.lower():
        #     errors['subtitle'] = "Subtitle cannot have the word 'blog'"
        
        # if 'blog' in self.slug.lower():
        #     errors['slug'] = "Slug cannot have the word 'blog'"
        
        # if errors:
        #     raise ValidationError(errors)