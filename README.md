# ODENN Outdoor Products - Static Website with Wagtail CMS

A static website built with Wagtail CMS for selling bike racks and outdoor products. The site can be edited through Wagtail's admin interface and then built as a static site for deployment.

## Features

- **Editable Home Page**: Edit the homepage content through Wagtail admin
- **Editable About Page**: Manage your about page content
- **Product Management**: Upload and manage products (bike racks and outdoor products)
- **Static Site Generation**: Build the site as static HTML for fast, secure hosting

## Setup Instructions

### 1. Install Dependencies

Create a virtual environment and install requirements:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Run Migrations

```bash
python manage.py migrate
```

### 3. Create a Superuser

```bash
python manage.py createsuperuser
```

This will allow you to access the Wagtail admin at `/admin/`

### 4. Create Initial Pages

After logging into the admin, you'll need to create:
- A Home Page (root page)
- An About Page (child of Home)
- A Product Index Page (child of Home)

### 5. Run the Development Server

```bash
python manage.py runserver
```

Visit `http://localhost:8000` to see your site and `http://localhost:8000/admin` to edit content.

## Building the Static Site

To generate a static version of your site:

```bash
python manage.py build
```

This will create a `build/` directory containing all static HTML files. You can deploy this directory to any static hosting service (Netlify, Vercel, GitHub Pages, etc.).

## Usage

### Adding Products

1. Go to `/admin/`
2. Navigate to Pages → Product Index Page
3. Click "Add child page" → "Product Page"
4. Fill in:
   - Title
   - Description
   - Price
   - SKU (optional)
   - Image
5. Publish the page

### Editing Home Page

1. Go to `/admin/`
2. Navigate to Pages → Home Page
3. Click "Edit"
4. Update the intro text and body content
5. Publish

### Editing About Page

1. Go to `/admin/`
2. Navigate to Pages → About Page
3. Click "Edit"
4. Update content
5. Publish

## Project Structure

```
ODENN/
├── oden_site/          # Django project settings
├── home/               # Home and About page models
├── products/           # Product models
├── templates/          # HTML templates
├── build/              # Generated static site (after running build)
├── media/              # Uploaded images and files
└── manage.py          # Django management script
```

## Notes

- The static site is generated using `wagtail-bakery`
- All published pages are included in the static build
- Media files (images) are copied to the build directory
- After building, you can deploy the `build/` directory to any static host

