from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from wagtail import hooks
from wagtail.admin.menu import MenuItem
from wagtail.admin.auth import require_admin_access
import csv
import io
from decimal import Decimal, InvalidOperation
from .models import ProductsListingPage, ProductIndexPage, ProductPage
from wagtail.models import Page


@hooks.register('register_admin_menu_item')
def register_csv_import_menu_item():
    """Register CSV import menu item in Wagtail admin"""
    return MenuItem(
        'Import Products',
        '/admin/products/import-csv/',
        classname='icon icon-download',
        order=1000
    )


@require_admin_access
def import_products_csv(request):
    """Wagtail admin view for CSV product import"""
    if request.method == 'POST' and 'csv_file' in request.FILES:
        csv_file = request.FILES['csv_file']
        
        # Read CSV file
        try:
            decoded_file = csv_file.read().decode('utf-8')
            csv_reader = csv.DictReader(io.StringIO(decoded_file))
            
            # Get or create Products Listing Page (must be under HomePage)
            products_listing = ProductsListingPage.objects.live().first()
            if not products_listing:
                # Get HomePage (must exist as root)
                from home.models import HomePage
                home_page = HomePage.objects.live().first()
                if not home_page:
                    messages.error(request, "Home Page must be created first. Please create a Home Page before importing products.")
                    return redirect('/admin/products/import-csv/')
                
                products_listing = ProductsListingPage(
                    title="Products",
                    slug="products"
                )
                home_page.add_child(instance=products_listing)
                products_listing.save_revision().publish()
            
            created_count = 0
            updated_count = 0
            errors = []
            
            for row_num, row in enumerate(csv_reader, start=2):  # Start at 2 (header is row 1)
                try:
                    category_name = row.get('product_category', '').strip()
                    product_name = row.get('product', '').strip()
                    price_str = row.get('price', '').strip()
                    
                    if not category_name or not product_name or not price_str:
                        errors.append(f"Row {row_num}: Missing required field (product_category, product, or price)")
                        continue
                    
                    # Parse price
                    try:
                        price = Decimal(price_str)
                    except (InvalidOperation, ValueError):
                        errors.append(f"Row {row_num}: Invalid price '{price_str}'")
                        continue
                    
                    # Get or create category
                    category = ProductIndexPage.objects.filter(
                        title=category_name,
                        path__startswith=products_listing.path
                    ).first()
                    
                    if not category:
                        category = ProductIndexPage(
                            title=category_name,
                            slug=category_name.lower().replace(' ', '-')
                        )
                        products_listing.add_child(instance=category)
                        category.save_revision().publish()
                        created_count += 1
                    
                    # Check if product already exists
                    existing_product = ProductPage.objects.filter(
                        title=product_name,
                        path__startswith=category.path
                    ).first()
                    
                    if existing_product:
                        # Update existing product
                        existing_product.price = price
                        existing_product.save_revision().publish()
                        updated_count += 1
                    else:
                        # Create new product
                        product = ProductPage(
                            title=product_name,
                            slug=product_name.lower().replace(' ', '-').replace('/', '-'),
                            price=price,
                            description=f"Product: {product_name}"
                        )
                        category.add_child(instance=product)
                        product.save_revision().publish()
                        created_count += 1
                        
                except Exception as e:
                    errors.append(f"Row {row_num}: {str(e)}")
                    continue
            
            # Show success/error messages
            if created_count > 0 or updated_count > 0:
                msg = f"Successfully imported {created_count} products"
                if updated_count > 0:
                    msg += f" and updated {updated_count} existing products"
                messages.success(request, msg)
            
            if errors:
                error_msg = f"Errors occurred: {'; '.join(errors[:10])}"
                if len(errors) > 10:
                    error_msg += f" (and {len(errors) - 10} more errors)"
                messages.warning(request, error_msg)
            
            return redirect('/admin/products/import-csv/')
        
        except Exception as e:
            messages.error(request, f"Error reading CSV file: {str(e)}")
    
    return render(request, 'products/import_csv.html', {
        'page_title': 'Import Products from CSV'
    })

