# Multiple Shopping Carts - Deployment Guide

## 🚀 PythonAnywhere Deployment

### Prerequisites
- PythonAnywhere account
- MySQL database (free tier available)

### Step 1: Upload Files
1. Upload all project files to your PythonAnywhere filesystem
2. Ensure the project structure is maintained

### Step 2: Database Setup
1. Go to PythonAnywhere Dashboard → Databases
2. Create a MySQL database named `moviesstore`
3. Note your database credentials

### Step 3: Update Settings
Update `moviesstore/settings.py` with your database credentials:

```python
DATABASES = {
    "default": {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'your_db_host.mysql.pythonanywhere-services.com',
        'PORT': '3306',
    }
}
```

### Step 4: Install Dependencies
In PythonAnywhere console:
```bash
pip3.10 install --user Django==5.0 mysqlclient==2.2.0 Pillow==10.0.0
```

### Step 5: Run Migrations
```bash
python3.10 manage.py migrate
```

### Step 6: Create Superuser
```bash
python3.10 manage.py createsuperuser
```

### Step 7: Collect Static Files
```bash
python3.10 manage.py collectstatic
```

### Step 8: Configure Web App
1. Go to Web tab in PythonAnywhere
2. Create new web app
3. Choose Django
4. Set source code path to your project directory
5. Set working directory to your project directory
6. Set WSGI file to `moviesstore/wsgi.py`

### Step 9: Update WSGI File
Update `moviesstore/wsgi.py`:
```python
import os
import sys

path = '/home/yourusername/yourprojectname'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'moviesstore.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

## ✅ Multiple Carts Features Ready for Deployment

The multiple shopping carts feature is fully cloud-ready:

- ✅ **Database Storage**: Uses MySQL models (Cart, CartItem)
- ✅ **No Localhost Dependencies**: All URLs are relative
- ✅ **Static Files**: Properly configured for cloud hosting
- ✅ **Media Files**: Uses Django's media handling
- ✅ **User Authentication**: Works across sessions
- ✅ **Cross-Platform**: Works on any Django hosting platform

## 🎯 Features Available After Deployment

1. **Multiple Carts**: Users can have Cart 1, Cart 2, Cart 3 + custom carts
2. **Cart Selection**: Dropdown when adding movies
3. **Cart Management**: View, switch, create, clear carts
4. **Individual Checkout**: Purchase specific carts
5. **User-Specific**: Each user has their own carts

## 🔧 Testing After Deployment

1. Create user accounts
2. Add movies to different carts
3. Switch between carts
4. Test checkout functionality
5. Verify cart persistence across sessions

The application is ready for production deployment!
