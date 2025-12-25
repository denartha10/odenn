# Deployment Summary

This document summarizes the changes made to prepare the project for Railway deployment.

## Changes Made

### 1. Production Dependencies Added
- `psycopg2-binary` - PostgreSQL database adapter
- `gunicorn` - Production WSGI server
- `whitenoise` - Static file serving
- `cloudinary` & `django-cloudinary-storage` - Cloud media storage
- `dj-database-url` - Database URL parsing

### 2. Settings Configuration
- Environment variable support for all sensitive settings
- Automatic PostgreSQL detection via `DATABASE_URL`
- Cloudinary integration for media files (images, documents)
- WhiteNoise for static file serving
- Production security settings (SSL, secure cookies, etc.)

### 3. Railway Configuration Files
- `Procfile` - Defines how Railway runs the app
- `runtime.txt` - Specifies Python version
- `.env.example` - Template for environment variables
- `.gitignore` - Excludes sensitive files from version control

### 4. Helper Scripts
- `generate_secret_key.py` - Generates secure Django secret keys

## Cost Breakdown

### Railway (Free Tier)
- **$5/month credit** included
- PostgreSQL: ~$5/month (uses free credit)
- Web service: ~$5/month (uses free credit)
- **Total: $0-5/month** (essentially free for small sites)

### Cloudinary (Free Tier)
- **25GB storage** free
- **25GB bandwidth/month** free
- No credit card required
- Perfect for images and documents

### Total Monthly Cost: **$0-5**

## Quick Deployment Checklist

1. ✅ Sign up for Railway (railway.app)
2. ✅ Sign up for Cloudinary (cloudinary.com) - FREE
3. ✅ Get Cloudinary credentials (Cloud Name, API Key, API Secret)
4. ✅ Generate SECRET_KEY using `python generate_secret_key.py`
5. ✅ Push code to GitHub/GitLab
6. ✅ Create Railway project and connect repository
7. ✅ Add PostgreSQL database in Railway
8. ✅ Set environment variables in Railway
9. ✅ Deploy and run migrations
10. ✅ Create superuser account
11. ✅ Access admin at `https://your-app.railway.app/admin/`

## Environment Variables Required

Set these in Railway's Variables tab:

```
SECRET_KEY=your-generated-secret-key
DEBUG=False
ALLOWED_HOSTS=your-app-name.railway.app
DATABASE_URL=auto-set-by-railway
BASE_URL=https://your-app-name.railway.app
WAGTAILADMIN_BASE_URL=https://your-app-name.railway.app
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
```

**Note:** `DATABASE_URL` is automatically set by Railway when you add PostgreSQL.

## Local Development

The project still works locally with SQLite:

1. Copy `.env.example` to `.env` (optional - defaults work for local dev)
2. Run `pip install -r requirements.txt`
3. Run `python manage.py migrate`
4. Run `python manage.py createsuperuser`
5. Run `python manage.py runserver`

Local development uses:
- SQLite database (no PostgreSQL needed)
- Local media storage (no Cloudinary needed)
- Development settings (DEBUG=True)

## Production vs Development

| Feature | Development | Production |
|---------|------------|------------|
| Database | SQLite | PostgreSQL (Railway) |
| Media Storage | Local files | Cloudinary |
| Static Files | Django dev server | WhiteNoise |
| Server | Django runserver | Gunicorn |
| SSL | No | Yes (automatic) |
| Debug | Enabled | Disabled |

## Troubleshooting

### Images not uploading
- Verify Cloudinary credentials in Railway variables
- Check Cloudinary dashboard to ensure account is active
- Ensure `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, and `CLOUDINARY_API_SECRET` are all set

### Database errors
- Ensure PostgreSQL is added to Railway project
- Check that `DATABASE_URL` is automatically set (Railway does this)
- Run migrations: `railway run python manage.py migrate`

### Static files not loading
- WhiteNoise should handle this automatically
- Check that `STATIC_ROOT` is set correctly
- Run `python manage.py collectstatic` if needed

### Can't access admin
- Ensure you created a superuser: `railway run python manage.py createsuperuser`
- Check `WAGTAILADMIN_BASE_URL` is set correctly
- Verify `ALLOWED_HOSTS` includes your Railway domain

## Next Steps

1. Follow the detailed deployment guide in `QUICKSTART.md`
2. Test the admin panel after deployment
3. Create a non-admin user for your client in Wagtail admin
4. Share admin URL and credentials securely with your client

## Support

For Railway-specific issues: https://docs.railway.app
For Cloudinary-specific issues: https://cloudinary.com/documentation
For Wagtail-specific issues: https://docs.wagtail.org

