"""
Management command to import products from CSV file.

Usage:
    python manage.py import_products products.csv
"""
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
import csv
import os
from decimal import Decimal, InvalidOperation
from products.models import ProductsListingPage, ProductIndexPage, ProductPage
from wagtail.models import Page


class Command(BaseCommand):
    help = 'Import products from a CSV file with columns: product_category, product, price'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to CSV file')
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be imported without actually importing',
        )

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']
        dry_run = options['dry_run']

        if not os.path.exists(csv_file_path):
            raise CommandError(f'CSV file not found: {csv_file_path}')

        # Get or create Products Listing Page (must be under HomePage)
        products_listing = ProductsListingPage.objects.live().first()
        if not products_listing:
            from home.models import HomePage
            home_page = HomePage.objects.live().first()
            if not home_page:
                raise CommandError('Home Page must be created first. Please create a Home Page before importing products.')
            
            products_listing = ProductsListingPage(
                title="Products",
                slug="products"
            )
            home_page.add_child(instance=products_listing)
            products_listing.save_revision().publish()
            self.stdout.write(self.style.SUCCESS(f'Created Products Listing Page'))

        created_categories = 0
        created_products = 0
        updated_products = 0
        errors = []

        try:
            with open(csv_file_path, 'r', encoding='utf-8') as f:
                csv_reader = csv.DictReader(f)
                
                # Validate headers
                required_headers = {'product_category', 'product', 'price'}
                if not required_headers.issubset(csv_reader.fieldnames or []):
                    raise CommandError(
                        f'CSV must have columns: product_category, product, price. '
                        f'Found: {", ".join(csv_reader.fieldnames or [])}'
                    )

                with transaction.atomic():
                    for row_num, row in enumerate(csv_reader, start=2):
                        try:
                            category_name = row.get('product_category', '').strip()
                            product_name = row.get('product', '').strip()
                            price_str = row.get('price', '').strip()

                            if not category_name or not product_name or not price_str:
                                errors.append(f"Row {row_num}: Missing required field")
                                continue

                            # Parse price
                            try:
                                price = Decimal(price_str)
                            except (InvalidOperation, ValueError):
                                errors.append(f"Row {row_num}: Invalid price '{price_str}'")
                                continue

                            if dry_run:
                                self.stdout.write(
                                    f"Would import: {product_name} ({category_name}) - ${price}"
                                )
                                continue

                            # Get or create category
                            category = ProductIndexPage.objects.filter(
                                title=category_name,
                                path__startswith=products_listing.path
                            ).first()

                            if not category:
                                category = ProductIndexPage(
                                    title=category_name,
                                    slug=category_name.lower().replace(' ', '-').replace('/', '-')
                                )
                                products_listing.add_child(instance=category)
                                category.save_revision().publish()
                                created_categories += 1
                                self.stdout.write(
                                    self.style.SUCCESS(f'Created category: {category_name}')
                                )

                            # Check if product already exists
                            existing_product = ProductPage.objects.filter(
                                title=product_name,
                                path__startswith=category.path
                            ).first()

                            if existing_product:
                                existing_product.price = price
                                existing_product.save_revision().publish()
                                updated_products += 1
                                self.stdout.write(
                                    self.style.WARNING(f'Updated: {product_name}')
                                )
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
                                created_products += 1
                                self.stdout.write(
                                    self.style.SUCCESS(f'Created: {product_name}')
                                )

                        except Exception as e:
                            errors.append(f"Row {row_num}: {str(e)}")
                            self.stdout.write(
                                self.style.ERROR(f'Error on row {row_num}: {str(e)}')
                            )

        except Exception as e:
            raise CommandError(f'Error reading CSV file: {str(e)}')

        # Summary
        self.stdout.write('\n' + '=' * 60)
        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN - No changes made'))
        else:
            self.stdout.write(self.style.SUCCESS(
                f'Import complete! Created {created_categories} categories, '
                f'{created_products} products, updated {updated_products} products'
            ))
        
        if errors:
            self.stdout.write(self.style.ERROR(f'\nErrors: {len(errors)}'))
            for error in errors[:10]:
                self.stdout.write(self.style.ERROR(f'  - {error}'))
            if len(errors) > 10:
                self.stdout.write(self.style.ERROR(f'  ... and {len(errors) - 10} more errors'))

