# ODENN Outdoor Products - Wagtail CMS Website

A modern, production-ready website built with Wagtail CMS for selling bike racks and outdoor products. The site is deployed on Railway with PostgreSQL and Cloudinary for media storage.

## Table of Contents

- [Features](#features)
- [Quick Start](#quick-start)
- [Local Development](#local-development)
- [Project Structure](#project-structure)
- [Content Management](#content-management)
- [CSV Product Import](#csv-product-import)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)
- [For Future Developers](#for-future-developers)

## Features

- **Editable Home Page**: Edit homepage content, hero background image, and body content through Wagtail admin
- **Editable About Page**: Manage your about page content with rich text and images
- **Product Management**: Upload and manage products with categories
- **CSV Product Import**: Mass upload products from CSV files
- **Contact Page**: Display contact information (phone, email, description)
- **Product Categories**: Organize products into categories with cover photos
- **Product Specifications**: Upload PDF specifications for products
- **Cloud Media Storage**: All images and documents stored on Cloudinary (free tier)
- **Production Ready**: Deployed on Railway with PostgreSQL and automatic SSL

## Quick Start

### Prerequisites

- Python 3.11+
- Git
- Railway account (for deployment)
- Cloudinary account (free tier available)

### Initial Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd ODENN
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser:**
   ```bash
   python manage.py createsuperuser
   ```

6. **Start development server:**
   ```bash
   python manage.py runserver
   ```

7. **Access admin panel:**
   - Open `http://localhost:8000/admin/`
   - Log in with your superuser credentials

## Local Development

### Development Environment

The project automatically detects the environment:
- **Local (no DATABASE_URL)**: Uses SQLite, local media storage, DEBUG=True
- **Production (DATABASE_URL set)**: Uses PostgreSQL, Cloudinary storage, DEBUG=False

### Creating Pages

After logging into the admin:

1. **Create Home Page:**
   - Go to Pages → Root
   - Click "Add child page" → "Home Page"
   - Fill in title, intro, and body content
   - Upload hero background image (optional)
   - Click "Publish"

2. **Create About Page:**
   - Go to Pages → Home Page
   - Click "Add child page" → "About Page"
   - Fill in content
   - Click "Publish"

3. **Create Products Structure:**
   - Go to Pages → Home Page
   - Click "Add child page" → "Products Listing Page"
   - Title it "Products"
   - Click "Publish"
   
   Then create categories:
   - Go to Pages → Products
   - Click "Add child page" → "Product Index Page"
   - Title it (e.g., "Cycle Parking")
   - Upload cover photo (optional)
   - Click "Publish"

4. **Add Products:**
   - Go to Pages → [Category Name]
   - Click "Add child page" → "Product Page"
   - Fill in title, description, price, SKU (optional)
   - Upload product image
   - Upload specification PDF (optional)
   - Click "Publish"

### Daily Workflow

1. **Edit content:**
   - Run `python manage.py runserver`
   - Go to `http://localhost:8000/admin/`
   - Edit pages or add products
   - Publish changes

2. **Preview changes:**
   - Visit `http://localhost:8000` to see your site

## CSV Product Import

You can mass upload products using a CSV file. This is especially useful for importing large product catalogs.

### CSV Format

Create a CSV file with the following columns:
- `product_category` - The name of the product category (will be created if it doesn't exist)
- `product` - The product name/title
- `price` - The product price (numeric, e.g., 199.99)

**Example CSV (`products.csv`):**
```csv
product_category,product,price
Cycle Parking,Premium Two-Tier Cycle Rack,299.99
Cycle Parking,Standard Cycle Rack,149.99
Cycle Hubs,Secure Cycle Hub,599.99
Cycle Hubs,Basic Cycle Hub,399.99
```

### How to Import

1. **Via Wagtail Admin (Recommended):**
   - Log into `/admin/`
   - Go to "Products" in the sidebar
   - Click "Import Products from CSV"
   - Upload your CSV file
   - Click "Import"
   - Products will be created under the appropriate categories

2. **Via Management Command:**
   ```bash
   python manage.py import_products products.csv
   ```

### Import Behavior

- **Categories**: If a category doesn't exist, it will be created as a `ProductIndexPage` under the main Products page
- **Products**: Each product will be created as a `ProductPage` under its category
- **Duplicates**: Products with the same title in the same category will be skipped (to avoid duplicates)
- **Validation**: Invalid prices or missing required fields will be reported

## Project Structure

```
ODENN/
├── oden_site/              # Django project settings
│   ├── settings.py         # Main settings (auto-detects dev/prod)
│   ├── urls.py             # URL configuration
│   └── wsgi.py             # WSGI application
├── home/                   # Home and About page models
│   ├── models.py          # HomePage, AboutPage, ContactPage
│   └── migrations/        # Database migrations
├── products/              # Product models
│   ├── models.py         # ProductsListingPage, ProductIndexPage, ProductPage
│   ├── admin.py          # Wagtail admin configuration
│   ├── views.py          # CSV import view
│   └── migrations/       # Database migrations
├── templates/            # HTML templates
│   ├── base.html        # Base template
│   ├── home/            # Home, About, Contact templates
│   └── products/         # Product templates
├── static/              # Static files (CSS, JS)
│   └── css/
│       └── main.css     # Main stylesheet
├── manage.py           # Django management script
├── requirements.txt    # Python dependencies
├── Procfile           # Railway deployment config
├── start.sh           # Startup script (runs migrations, creates superuser)
├── create_superuser.py # Auto-creates superuser if none exists
└── README.md          # This file
```

## Content Management

### Adding Products Manually

1. Go to `/admin/`
2. Navigate to Pages → [Your Category]
3. Click "Add child page" → "Product Page"
4. Fill in:
   - **Title**: Product name
   - **Description**: Rich text description
   - **Price**: Product price
   - **SKU**: Optional product SKU
   - **Image**: Main product image
   - **Specification PDF**: Optional downloadable PDF
5. Click "Publish"

### Editing Pages

1. Go to `/admin/`
2. Navigate to Pages → [Page Name]
3. Click "Edit"
4. Update content
5. Click "Publish"

### Managing Images

- All images are stored on Cloudinary (production) or locally (development)
- Images are automatically optimized and resized
- You can upload images through the Wagtail admin interface

## Deployment

### Production Deployment on Railway

The site is configured for deployment on Railway with:
- **PostgreSQL** database (automatically provisioned)
- **Cloudinary** for media storage (free tier: 25GB)
- **Automatic SSL** certificates
- **Auto-deployment** from GitHub

#### Deployment Steps

1. **Set up Cloudinary** (free account):
   - Sign up at [cloudinary.com](https://cloudinary.com/users/register_free)
   - Get your Cloud Name, API Key, and API Secret

2. **Deploy to Railway:**
   - Push code to GitHub
   - Create new project on [railway.app](https://railway.app)
   - Connect your GitHub repository
   - Add PostgreSQL database
   - Set environment variables (see below)

3. **Environment Variables** (set in Railway):
   ```
   SECRET_KEY=your-generated-secret-key
   DEBUG=False
   ALLOWED_HOSTS=your-app-name.railway.app
   BASE_URL=https://your-app-name.railway.app
   WAGTAILADMIN_BASE_URL=https://your-app-name.railway.app
   CLOUDINARY_CLOUD_NAME=your-cloud-name
   CLOUDINARY_API_KEY=your-api-key
   CLOUDINARY_API_SECRET=your-api-secret
   ```
   
   **Note:** `DATABASE_URL` is automatically set by Railway.

4. **Generate Secret Key:**
   ```bash
   python generate_secret_key.py
   ```

5. **Access your site:**
   - Site: `https://your-app-name.railway.app`
   - Admin: `https://your-app-name.railway.app/admin/`

### Cost Breakdown

- **Railway**: $0-5/month (free tier includes $5 credit)
- **Cloudinary**: FREE (25GB storage, 25GB bandwidth/month)
- **Total**: Essentially free for small to medium sites

## Troubleshooting

### Common Issues

**Issue: Can't access admin panel**
- Ensure you created a superuser: `python manage.py createsuperuser`
- Check that `WAGTAILADMIN_BASE_URL` is set correctly
- Verify `ALLOWED_HOSTS` includes your domain

**Issue: Images not uploading**
- **Local**: Check that `media/` directory exists and is writable
- **Production**: Verify Cloudinary credentials in Railway variables
- Check Cloudinary dashboard to ensure account is active

**Issue: Database errors**
- **Local**: Run `python manage.py migrate`
- **Production**: Ensure PostgreSQL is added to Railway project
- Check that `DATABASE_URL` is automatically set (Railway does this)

**Issue: Site shows 404 or redirect loop**
- Ensure you have a Home Page set as the root page
- Go to Settings → Sites in admin and set the root page
- Make sure pages are published (not in draft)

**Issue: Static files not loading**
- Run `python manage.py collectstatic`
- Check that `STATIC_ROOT` is set correctly
- WhiteNoise handles static files automatically in production

### Getting Help

- **Railway Issues**: https://docs.railway.app
- **Cloudinary Issues**: https://cloudinary.com/documentation
- **Wagtail Issues**: https://docs.wagtail.org
- **Django Issues**: https://docs.djangoproject.com

## For Future Developers

### Getting Started

1. **Clone and set up:**
   ```bash
   git clone <repository-url>
   cd ODENN
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver
   ```

2. **Understand the structure:**
   - `home/` - Home, About, and Contact page models
   - `products/` - Product listing, category, and product page models
   - `templates/` - HTML templates using Django/Wagtail templating
   - `static/css/` - Stylesheet (modern, responsive design)

### Key Technologies

- **Django 4.2** - Web framework
- **Wagtail 5.2+** - CMS built on Django
- **PostgreSQL** - Production database (SQLite for local dev)
- **Cloudinary** - Media storage (local files for dev)
- **WhiteNoise** - Static file serving
- **Gunicorn** - Production WSGI server

### Making Changes

**Adding a new page type:**
1. Create a model in `home/models.py` or `products/models.py`
2. Run `python manage.py makemigrations`
3. Run `python manage.py migrate`
4. Create a template in `templates/`
5. Add the page type to Wagtail admin

**Modifying styles:**
- Edit `static/css/main.css`
- CSS uses modern design principles with CSS variables
- Fully responsive with mobile-first approach

**Adding features:**
- Follow Django/Wagtail best practices
- Keep code organized in appropriate apps
- Write migrations for database changes
- Test locally before deploying

### Environment Variables

The app uses environment variables for configuration:

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | `django-insecure-change-this-in-production` |
| `DEBUG` | Debug mode | `True` (local), `False` (production) |
| `ALLOWED_HOSTS` | Allowed hostnames | `*` |
| `DATABASE_URL` | Database connection | SQLite (local), PostgreSQL (production) |
| `BASE_URL` | Site base URL | `http://localhost:8000` |
| `WAGTAILADMIN_BASE_URL` | Admin base URL | Same as `BASE_URL` |
| `CLOUDINARY_CLOUD_NAME` | Cloudinary cloud name | (local uses file storage) |
| `CLOUDINARY_API_KEY` | Cloudinary API key | (local uses file storage) |
| `CLOUDINARY_API_SECRET` | Cloudinary API secret | (local uses file storage) |

### Database Migrations

When modifying models:
```bash
python manage.py makemigrations
python manage.py migrate
```

### Static Site Generation

To build a static version of the site:
```bash
python manage.py build
```

This creates a `build/` directory with static HTML files that can be deployed to any static hosting service.

### Code Style

- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add comments for complex logic
- Keep functions focused and small
- Use Django/Wagtail conventions

### Security Notes

- Never commit `SECRET_KEY` or other sensitive data
- Use environment variables for all secrets
- Keep dependencies updated
- Review security settings in `settings.py`

### Support Resources

- **Wagtail Documentation**: https://docs.wagtail.org/
- **Django Documentation**: https://docs.djangoproject.com/
- **Railway Documentation**: https://docs.railway.app/
- **Cloudinary Documentation**: https://cloudinary.com/documentation

---

**Last Updated**: December 2025
**Maintained by**: ODENN Development Team
