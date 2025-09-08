#!/bin/bash

# Mesa Global - Export Data Script
# Run this script to export current data from the server

echo "📤 Exporting data from Mesa Global server..."

cd /var/www/mesa-global
source venv/bin/activate

# Create data directory if it doesn't exist
mkdir -p data

# Export data
echo "🔄 Exporting regions..."
export DJANGO_SETTINGS_MODULE=mesa_global.settings_production
python manage.py dumpdata blog.Region --indent 2 > data/regions.json

echo "🔄 Exporting categories..."
python manage.py dumpdata blog.Category --indent 2 > data/categories.json

echo "🔄 Exporting tags..."
python manage.py dumpdata blog.Tag --indent 2 > data/tags.json

echo "🔄 Exporting recipes..."
python manage.py dumpdata blog.Recipe --indent 2 > data/recipes.json

echo "🔄 Exporting articles..."
python manage.py dumpdata blog.Article --indent 2 > data/articles.json

# Combine all data
echo "🔄 Combining all data..."
cat data/regions.json data/categories.json data/tags.json data/recipes.json data/articles.json > data/data_backup.json

# Remove individual files
rm data/regions.json data/categories.json data/tags.json data/recipes.json data/articles.json

echo "✅ Data exported successfully to data/data_backup.json"
echo "📊 File size: $(du -h data/data_backup.json | cut -f1)"

# Commit to git
echo "🔄 Committing to git..."
git add data/data_backup.json
git commit -m "Update data backup from server"
git push origin main

echo "🎉 Data export and backup completed!"
