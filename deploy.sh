#!/bin/bash

# Mesa Global - Production Deployment Script
# Server: 62.60.157.18

echo "🚀 Starting Mesa Global deployment..."

# Update system packages
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install required packages
echo "🔧 Installing required packages..."
sudo apt install -y python3-pip python3-venv python3-dev nginx postgresql postgresql-contrib libpq-dev

# Create project directory
echo "📁 Creating project directory..."
sudo mkdir -p /var/www/mesa-global
sudo chown -R $USER:$USER /var/www/mesa-global
cd /var/www/mesa-global

# Clone repository
echo "📥 Cloning repository..."
git clone https://github.com/beiseek/mesa-global.git .

# Create virtual environment
echo "🐍 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "📚 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Configure PostgreSQL
echo "🗄️ Configuring PostgreSQL..."
sudo -u postgres psql -c "CREATE DATABASE mesa_global;"
sudo -u postgres psql -c "CREATE USER mesa_user WITH PASSWORD 'mesa_global_2024';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE mesa_global TO mesa_user;"
sudo -u postgres psql -c "ALTER USER mesa_user CREATEDB;"

# Create production settings
echo "⚙️ Creating production settings..."
cat > mesa_global/settings_production.py << EOF
from .settings import *
import os

DEBUG = False
ALLOWED_HOSTS = ['62.60.157.18', 'localhost', '127.0.0.1']

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mesa_global',
        'USER': 'mesa_user',
        'PASSWORD': 'mesa_global_2024',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Static files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Security settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/var/log/mesa-global/django.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
EOF

# Create log directory
sudo mkdir -p /var/log/mesa-global
sudo chown -R $USER:$USER /var/log/mesa-global

# Run migrations
echo "🔄 Running database migrations..."
export DJANGO_SETTINGS_MODULE=mesa_global.settings_production
python manage.py migrate

# Create superuser (will prompt for credentials)
echo "👤 Creating superuser..."
python manage.py createsuperuser

# Load initial data
echo "📊 Loading initial data..."
python manage.py load_initial_data

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Create Gunicorn service
echo "🔧 Creating Gunicorn service..."
sudo tee /etc/systemd/system/mesa-global.service > /dev/null << EOF
[Unit]
Description=Mesa Global Django App
After=network.target

[Service]
User=$USER
Group=www-data
WorkingDirectory=/var/www/mesa-global
Environment="PATH=/var/www/mesa-global/venv/bin"
Environment="DJANGO_SETTINGS_MODULE=mesa_global.settings_production"
ExecStart=/var/www/mesa-global/venv/bin/gunicorn --workers 3 --bind unix:/var/www/mesa-global/mesa-global.sock mesa_global.wsgi:application
ExecReload=/bin/kill -s HUP \$MAINPID
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF

# Configure Nginx
echo "🌐 Configuring Nginx..."
sudo tee /etc/nginx/sites-available/mesa-global > /dev/null << EOF
server {
    listen 80;
    server_name 62.60.157.18;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /var/www/mesa-global;
    }
    location /media/ {
        root /var/www/mesa-global;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/mesa-global/mesa-global.sock;
    }
}
EOF

# Enable site
sudo ln -s /etc/nginx/sites-available/mesa-global /etc/nginx/sites-enabled
sudo nginx -t

# Start services
echo "🚀 Starting services..."
sudo systemctl daemon-reload
sudo systemctl start mesa-global
sudo systemctl enable mesa-global
sudo systemctl restart nginx

# Set permissions
sudo chown -R $USER:www-data /var/www/mesa-global
sudo chmod -R 755 /var/www/mesa-global

echo "✅ Deployment completed successfully!"
echo "🌐 Your site should be available at: http://62.60.157.18"
echo "👤 Admin panel: http://62.60.157.18/admin"
echo ""
echo "📋 Useful commands:"
echo "  - Check service status: sudo systemctl status mesa-global"
echo "  - View logs: sudo journalctl -u mesa-global -f"
echo "  - Restart service: sudo systemctl restart mesa-global"
echo "  - Update code: cd /var/www/mesa-global && git pull && sudo systemctl restart mesa-global"
