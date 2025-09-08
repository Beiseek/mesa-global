#!/bin/bash

# Mesa Global - Update Script
# Run this script to update the project on the server

echo "🔄 Updating Mesa Global..."

cd /var/www/mesa-global

# Pull latest changes
echo "📥 Pulling latest changes from GitHub..."
git pull origin main

# Activate virtual environment
source venv/bin/activate

# Install/update dependencies
echo "📚 Updating dependencies..."
pip install -r requirements.txt

# Run migrations
echo "🔄 Running database migrations..."
export DJANGO_SETTINGS_MODULE=mesa_global.settings_production
python manage.py migrate

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Restart services
echo "🔄 Restarting services..."
sudo systemctl restart mesa-global
sudo systemctl restart nginx

echo "✅ Update completed successfully!"
echo "🌐 Site updated at: http://62.60.157.18"
