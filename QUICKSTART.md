# Quick Start Guide

## Initial Setup (One-time)

1. **Install dependencies:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

3. **Create admin user:**
   ```bash
   python manage.py createsuperuser
   ```
   Follow the prompts to create your admin account.

4. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

5. **Access the admin:**
   - Open `http://localhost:8000/admin/`
   - Log in with your superuser credentials

## Creating Your First Pages

After logging into the admin:

1. **Create Home Page:**
   - Go to Pages → Root
   - Click "Add child page"
   - Select "Home Page"
   - Fill in the title (e.g., "Home")
   - Add intro text and content
   - Click "Publish"

2. **Create About Page:**
   - Go to Pages → Home Page
   - Click "Add child page"
   - Select "About Page"
   - Fill in content
   - Click "Publish"

3. **Create Products Index:**
   - Go to Pages → Home Page
   - Click "Add child page"
   - Select "Product Index Page"
   - Title it "Products"
   - Click "Publish"

4. **Add Your First Product:**
   - Go to Pages → Products
   - Click "Add child page"
   - Select "Product Page"
   - Fill in:
     - Title (e.g., "Premium Bike Rack")
     - Description
     - Price
     - SKU (optional)
     - Upload an image
   - Click "Publish"

## Building the Static Site

Once you've added content and are ready to deploy:

```bash
python manage.py build
```

Or use the build script:
```bash
./build_static.sh
```

The static site will be generated in the `build/` directory. You can deploy this entire directory to:
- Netlify
- Vercel
- GitHub Pages
- Any static hosting service

## Daily Workflow

1. **Edit content:**
   - Run `python manage.py runserver`
   - Go to `http://localhost:8000/admin/`
   - Edit pages or add products
   - Publish changes

2. **Preview changes:**
   - Visit `http://localhost:8000` to see your site

3. **Build static site:**
   - Run `python manage.py build` when ready to deploy
   - Deploy the `build/` directory

## Deploying to Railway (Production)

Railway is a simple hosting platform that makes it easy to deploy your Wagtail CMS. The free tier includes $5/month credit, which is enough for a small site.

### Prerequisites

1. **Railway Account**: Sign up at [railway.app](https://railway.app) (free)
2. **Cloudinary Account**: Sign up at [cloudinary.com](https://cloudinary.com/users/register_free) for free media storage (25GB free tier)

### Step 1: Set Up Cloudinary (Free Media Storage)

1. Go to [cloudinary.com](https://cloudinary.com/users/register_free) and create a free account
2. Once logged in, go to your Dashboard
3. Copy these three values:
   - **Cloud Name** (e.g., `dxyz123abc`)
   - **API Key** (e.g., `123456789012345`)
   - **API Secret** (e.g., `abcdefghijklmnopqrstuvwxyz`)

Keep these handy - you'll need them in Step 3.

### Step 2: Prepare Your Code

1. **Generate a Secret Key** (for production security):
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(50))"
   ```
   Copy this value - you'll need it in Step 3.

2. **Push your code to GitHub** (or GitLab/Bitbucket):
   - Create a repository on GitHub
   - Push your code:
     ```bash
     git init
     git add .
     git commit -m "Initial commit"
     git remote add origin https://github.com/yourusername/your-repo.git
     git push -u origin main
     ```

### Step 3: Deploy to Railway

1. **Create a New Project on Railway:**
   - Go to [railway.app](https://railway.app)
   - Click "New Project"
   - Select "Deploy from GitHub repo" (or "Empty Project" if you prefer to upload manually)
   - Choose your repository

2. **Add PostgreSQL Database:**
   - In your Railway project, click "New"
   - Select "Database" → "Add PostgreSQL"
   - Railway will automatically create a PostgreSQL database
   - The `DATABASE_URL` will be automatically set as an environment variable

3. **Set Environment Variables:**
   - In your Railway project, go to the "Variables" tab
   - Add these environment variables:

   ```
   SECRET_KEY=your-secret-key-from-step-1
   DEBUG=False
   ALLOWED_HOSTS=your-app-name.railway.app
   BASE_URL=https://your-app-name.railway.app
   WAGTAILADMIN_BASE_URL=https://your-app-name.railway.app
   CLOUDINARY_CLOUD_NAME=your-cloud-name-from-cloudinary
   CLOUDINARY_API_KEY=your-api-key-from-cloudinary
   CLOUDINARY_API_SECRET=your-api-secret-from-cloudinary
   ```

   **Note:** Replace `your-app-name.railway.app` with your actual Railway app URL (you'll see this after deployment).

4. **Deploy:**
   - Railway will automatically detect your `Procfile` and start deploying
   - Wait for the deployment to complete (usually 2-3 minutes)
   - Your app will be live at `https://your-app-name.railway.app`

5. **Run Migrations and Create Admin User:**
   - In Railway, go to your service
   - Click on the "Deployments" tab
   - Click on the latest deployment
   - Open the "Logs" tab
   - Click "Run Command" or use Railway's CLI:
     ```bash
     railway run python manage.py migrate
     railway run python manage.py createsuperuser
     ```
   
   Or use Railway's web interface:
   - Go to your service → "Settings" → "Deploy" → "Run Command"
   - Run: `python manage.py migrate`
   - Run: `python manage.py createsuperuser` (follow prompts)

6. **Access Your Admin Panel:**
   - Visit `https://your-app-name.railway.app/admin/`
   - Log in with the superuser credentials you just created
   - Start editing your content!

### Step 4: Custom Domain (Optional)

1. In Railway, go to your service → "Settings" → "Networking"
2. Click "Generate Domain" or add your custom domain
3. Update `ALLOWED_HOSTS` in Railway variables to include your custom domain
4. Update `BASE_URL` and `WAGTAILADMIN_BASE_URL` to your custom domain

### Cost Breakdown

- **Railway**: Free tier includes $5/month credit
  - PostgreSQL: ~$5/month (uses your free credit)
  - Web service: ~$5/month (uses your free credit)
  - **Total: ~$0-5/month** (depending on usage)
  
- **Cloudinary**: **FREE** (25GB storage, 25GB bandwidth/month)
  - Perfect for images and documents
  - No credit card required

- **Total Monthly Cost: $0-5** (essentially free for small sites)

### Daily Workflow (After Deployment)

1. **Edit Content:**
   - Visit `https://your-app-name.railway.app/admin/`
   - Log in with your admin credentials
   - Edit pages, add products, upload images
   - Click "Publish" to make changes live

2. **View Your Site:**
   - Visit `https://your-app-name.railway.app` to see your live site
   - Changes are instant after publishing

### Troubleshooting

**Issue: Can't access admin panel**
- Make sure you ran `python manage.py createsuperuser` on Railway
- Check that `WAGTAILADMIN_BASE_URL` is set correctly

**Issue: Images not uploading**
- Verify your Cloudinary credentials are correct in Railway variables
- Check Cloudinary dashboard to ensure your account is active

**Issue: Database errors**
- Make sure PostgreSQL is added to your Railway project
- Check that `DATABASE_URL` is automatically set (Railway does this)

**Issue: Site not loading**
- Check Railway logs for errors
- Verify all environment variables are set correctly
- Make sure `ALLOWED_HOSTS` includes your Railway domain

### Sharing Access with Your Client

1. **Create a Wagtail User for Your Client:**
   - Go to `/admin/users/` in your Wagtail admin
   - Click "Add user"
   - Create a user with "Editor" or "Moderator" permissions
   - Share the login credentials securely

2. **Share the Admin URL:**
   - Give them: `https://your-app-name.railway.app/admin/`
   - They can log in and edit content without touching code

### Future Development

If you need to give the code to another developer:

1. **Share the Repository:**
   - Give them access to your GitHub/GitLab repository
   - Or share the code via cloud storage (Dropbox, Google Drive, etc.)

2. **Share Environment Variables:**
   - Export Railway environment variables or share the `.env.example` file
   - They can set up their own Railway project or run locally

3. **Local Development:**
   - They can clone the repo
   - Copy `.env.example` to `.env` and fill in values
   - Run `pip install -r requirements.txt`
   - Run `python manage.py migrate`
   - Run `python manage.py runserver`

## Tips

- Always publish pages after editing (draft pages won't appear on the live site)
- Images uploaded through Wagtail are automatically stored on Cloudinary
- The site is live 24/7 on Railway - no need to run a server yourself
- Railway automatically handles SSL certificates (HTTPS)
- You can view deployment logs in Railway dashboard if something goes wrong
- Railway automatically redeploys when you push code to GitHub (if connected)

