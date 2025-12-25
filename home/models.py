from django.db import models
from django.core.exceptions import ValidationError
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock


class HomePage(Page):
    """Home page model - Only one instance allowed, must be root page"""
    
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
    
    # Only allow HomePage to be created as root (depth=1)
    parent_page_types = []
    
    # HomePage can have AboutPage, ContactPage, and ProductsListingPage as children
    subpage_types = ['home.AboutPage', 'home.ContactPage', 'products.ProductsListingPage']
    
    content_panels = Page.content_panels + [
        FieldPanel('hero_background'),
        FieldPanel('intro'),
        FieldPanel('body'),
    ]
    
    def clean(self):
        super().clean()
        # Ensure only one HomePage exists
        if self.pk is None:  # New instance
            if HomePage.objects.exists():
                raise ValidationError({
                    'title': 'Only one Home Page can exist. Please edit the existing Home Page instead.'
                })
        else:  # Editing existing instance
            if HomePage.objects.exclude(pk=self.pk).exists():
                raise ValidationError({
                    'title': 'Only one Home Page can exist. Please edit the existing Home Page instead.'
                })
    
    class Meta:
        verbose_name = "Home Page"


class AboutPage(Page):
    """About page model - Only one instance allowed, must be child of HomePage"""
    
    intro = RichTextField(blank=True, help_text="Introduction text")
    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
    ], use_json_field=True, blank=True)
    
    # AboutPage can only be a child of HomePage
    parent_page_types = ['home.HomePage']
    
    # AboutPage cannot have children
    subpage_types = []
    
    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('body'),
    ]
    
    def clean(self):
        super().clean()
        # Ensure only one AboutPage exists
        if self.pk is None:  # New instance
            if AboutPage.objects.exists():
                raise ValidationError({
                    'title': 'Only one About Page can exist. Please edit the existing About Page instead.'
                })
        else:  # Editing existing instance
            if AboutPage.objects.exclude(pk=self.pk).exists():
                raise ValidationError({
                    'title': 'Only one About Page can exist. Please edit the existing About Page instead.'
                })
    
    class Meta:
        verbose_name = "About Page"


class ContactPage(Page):
    """Contact page model - Only one instance allowed, must be child of HomePage"""
    
    description = RichTextField(blank=True, help_text="Contact page description and information")
    phone = models.CharField(max_length=50, blank=True, help_text="Phone number")
    email = models.EmailField(blank=True, help_text="Email address")
    
    # ContactPage can only be a child of HomePage
    parent_page_types = ['home.HomePage']
    
    # ContactPage cannot have children
    subpage_types = []
    
    content_panels = Page.content_panels + [
        FieldPanel('description'),
        FieldPanel('phone'),
        FieldPanel('email'),
    ]
    
    def clean(self):
        super().clean()
        # Ensure only one ContactPage exists
        if self.pk is None:  # New instance
            if ContactPage.objects.exists():
                raise ValidationError({
                    'title': 'Only one Contact Page can exist. Please edit the existing Contact Page instead.'
                })
        else:  # Editing existing instance
            if ContactPage.objects.exclude(pk=self.pk).exists():
                raise ValidationError({
                    'title': 'Only one Contact Page can exist. Please edit the existing Contact Page instead.'
                })
    
    class Meta:
        verbose_name = "Contact Page"

