# Setup Notes

## Important: Fixing the 404 Error

If you're getting a 404 when visiting `localhost:8000`, you need to:

1. **Set the Home Page as the Root Page:**
   - Go to `/admin/`
   - Navigate to Settings → Sites
   - Edit the default site
   - Set the "Root page" to your Home Page
   - Save

2. **Make sure your Home Page is published:**
   - Go to Pages in the admin
   - Find your Home Page
   - Make sure it's published (not in draft)

## Running Migrations for Contact Page

After adding the ContactPage model, you need to create and run migrations:

```bash
python manage.py makemigrations home
python manage.py migrate
```

## Creating Pages

Make sure to create pages in this order:
1. **Home Page** - Set as root page
2. **About Page** - Child of Home
3. **Product Index Page** - Child of Home (slug: "products")
4. **Contact Page** - Child of Home (slug: "contact")
5. **Product Pages** - Children of Product Index Page

## Page Slugs

For the navigation to work correctly, make sure your pages have these slugs:
- Home Page: "/" (root)
- Products: "/products/"
- About: "/about/"
- Contact: "/contact/"

