from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock


class HomePage(Page):
    """Home page model"""
    
    hero_background = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="Hero section background image"
    )
    intro = RichTextField(blank=True, help_text="Introduction text for the homepage")
    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
    ], use_json_field=True, blank=True)
    
    content_panels = Page.content_panels + [
        FieldPanel('hero_background'),
        FieldPanel('intro'),
        FieldPanel('body'),
    ]
    
    class Meta:
        verbose_name = "Home Page"


class AboutPage(Page):
    """About page model"""
    
    intro = RichTextField(blank=True, help_text="Introduction text")
    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
    ], use_json_field=True, blank=True)
    
    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('body'),
    ]
    
    class Meta:
        verbose_name = "About Page"


class ContactPage(Page):
    """Contact page model"""
    
    description = RichTextField(blank=True, help_text="Contact page description and information")
    phone = models.CharField(max_length=50, blank=True, help_text="Phone number")
    email = models.EmailField(blank=True, help_text="Email address")
    
    content_panels = Page.content_panels + [
        FieldPanel('description'),
        FieldPanel('phone'),
        FieldPanel('email'),
    ]
    
    class Meta:
        verbose_name = "Contact Page"

