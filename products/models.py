from django.db import models
from django.core.exceptions import ValidationError
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from wagtail.search import index


class ProductsListingPage(Page):
    """Main products page that lists all product categories - Only one instance allowed"""
    
    intro = RichTextField(blank=True, help_text="Text to describe the products page")
    
    # ProductsListingPage can only be a child of HomePage
    parent_page_types = ['home.HomePage']
    
    # ProductsListingPage can only have ProductIndexPage as children
    subpage_types = ['products.ProductIndexPage']
    
    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]
    
    def get_context(self, request):
        context = super().get_context(request)
        # Get all ProductIndexPage children (categories)
        categories = ProductIndexPage.objects.live().public().filter(
            path__startswith=self.path
        ).order_by('title')
        context['categories'] = categories
        
        # Get all products for search functionality
        all_products = ProductPage.objects.live().public().filter(
            path__startswith=self.path
        ).select_related('image').order_by('title')
        
        # Prepare product data for JavaScript
        import json
        from django.utils.html import strip_tags
        
        products_data = []
        for product in all_products:
            # Extract plain text from RichTextField
            description_text = ''
            if product.description:
                if hasattr(product.description, 'source'):
                    # It's a RichText object
                    description_text = strip_tags(str(product.description))
                elif hasattr(product.description, 'plain_text'):
                    # It has plain_text method
                    description_text = product.description.plain_text()
                else:
                    # It's already a string or can be converted
                    description_text = strip_tags(str(product.description))
            
            products_data.append({
                'id': product.id,
                'title': product.title,
                'price': str(product.price),
                'description': description_text,
                'sku': product.sku or '',
                'url': product.url,
                'category': product.get_parent().title if product.get_parent() else '',
                'image_url': product.image.file.url if product.image and product.image.file else '',
            })
        
        context['all_products_json'] = json.dumps(products_data)
        return context
    
    def clean(self):
        super().clean()
        # Ensure only one ProductsListingPage exists
        if self.pk is None:  # New instance
            if ProductsListingPage.objects.exists():
                raise ValidationError({
                    'title': 'Only one Products Listing Page can exist. Please edit the existing Products Listing Page instead.'
                })
        else:  # Editing existing instance
            if ProductsListingPage.objects.exclude(pk=self.pk).exists():
                raise ValidationError({
                    'title': 'Only one Products Listing Page can exist. Please edit the existing Products Listing Page instead.'
                })
    
    class Meta:
        verbose_name = "Products Listing Page"


class ProductIndexPage(Page):
    """Index page for a specific product category - Can only be child of ProductsListingPage"""
    
    cover_photo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="Cover photo/hero image for this category"
    )
    intro = RichTextField(blank=True, help_text="Text to describe this product category")
    
    # ProductIndexPage can only be a child of ProductsListingPage
    parent_page_types = ['products.ProductsListingPage']
    
    # ProductIndexPage can only have ProductPage as children
    subpage_types = ['products.ProductPage']
    
    content_panels = Page.content_panels + [
        FieldPanel('cover_photo'),
        FieldPanel('intro'),
    ]
    
    def get_context(self, request):
        context = super().get_context(request)
        # Only show products that are direct children of this category
        products = ProductPage.objects.live().public().filter(
            path__startswith=self.path
        ).order_by('-first_published_at')
        context['products'] = products
        return context
    
    class Meta:
        verbose_name = "Product Category Page"


class ProductPage(Page):
    """Product page model for bike racks and outdoor products - Can only be child of ProductIndexPage"""
    
    description = RichTextField(blank=True, help_text="Product description")
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Product price")
    sku = models.CharField(max_length=50, blank=True, help_text="Product SKU")
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="Main product image"
    )
    specification_pdf = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="Product specification PDF"
    )
    
    # ProductPage can only be a child of ProductIndexPage
    parent_page_types = ['products.ProductIndexPage']
    
    # ProductPage cannot have children
    subpage_types = []
    
    search_fields = Page.search_fields + [
        index.SearchField('description'),
        index.SearchField('sku'),
    ]
    
    content_panels = Page.content_panels + [
        FieldPanel('description'),
        FieldPanel('price'),
        FieldPanel('sku'),
        FieldPanel('image'),
        FieldPanel('specification_pdf'),
    ]
    
    
    class Meta:
        verbose_name = "Product Page"
        verbose_name_plural = "Product Pages"

