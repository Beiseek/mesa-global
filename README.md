# Mesa Global - Multicultural Gastronomic Blog

A beautiful Django website for a global multicultural gastronomic blog that unites recipes, stories, and cultural traditions from different countries.

## Features

- 🌍 **Multicultural Content**: Recipes and stories from Asia, Europe, Africa, Latin America, and Middle East
- 🍳 **Recipe Management**: Detailed recipes with ingredients, instructions, and cultural context
- 📖 **Story Platform**: Personal stories, interviews, and cultural essays
- 🎨 **Beautiful Design**: Ethnic accents with orange color scheme and responsive design
- 📱 **Mobile Friendly**: Adaptive design for mobile, tablet, and desktop
- 🔍 **Filtering System**: Filter by regions, categories, and tags
- 📝 **Content Submission**: Form for users to submit their recipes and stories
- 🔧 **Admin Panel**: Easy content management through Django admin
- 🚀 **SEO Optimized**: Meta tags and sitemap for search engines

## Technology Stack

- **Backend**: Django 5.2.1
- **Frontend**: Bootstrap 5, Font Awesome, AOS animations
- **Database**: SQLite (development), PostgreSQL (production)
- **Python**: 3.13+
- **Rich Text**: CKEditor for content editing

## Installation

### Prerequisites

- Python 3.13+
- pip
- Git

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/beiseek/mesa-global.git
   cd mesa-global
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Load initial data**
   ```bash
   python manage.py load_initial_data
   ```

7. **Collect static files**
   ```bash
   python manage.py collectstatic
   ```

8. **Run development server**
   ```bash
   python manage.py runserver
   ```

9. **Access the application**
   - Main site: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## Production Deployment

### Server Setup

1. **Install system dependencies**
   ```bash
   sudo apt update
   sudo apt install python3-pip python3-venv nginx postgresql postgresql-contrib
   ```

2. **Clone and setup project**
   ```bash
   git clone https://github.com/beiseek/mesa-global.git
   cd mesa-global
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configure database**
   ```bash
   sudo -u postgres createdb mesa_global
   sudo -u postgres createuser mesa_user
   sudo -u postgres psql -c "ALTER USER mesa_user PASSWORD 'your_password';"
   sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE mesa_global TO mesa_user;"
   ```

4. **Update settings for production**
   - Set `DEBUG = False`
   - Configure `ALLOWED_HOSTS`
   - Update database settings for PostgreSQL
   - Set proper `SECRET_KEY`

5. **Run migrations and collect static**
   ```bash
   python manage.py migrate
   python manage.py collectstatic --noinput
   python manage.py load_initial_data
   ```

6. **Configure Gunicorn**
   ```bash
   gunicorn --bind 0.0.0.0:8000 mesa_global.wsgi:application
   ```

7. **Configure Nginx**
   - Set up reverse proxy to Gunicorn
   - Serve static files
   - Configure SSL certificate

## Project Structure

```
mesa-global/
├── blog/                    # Main Django app
│   ├── models.py           # Database models
│   ├── views.py            # View functions
│   ├── urls.py             # URL patterns
│   ├── admin.py            # Admin configuration
│   └── management/         # Custom management commands
├── mesa_global/            # Django project settings
│   ├── settings.py         # Main settings
│   ├── urls.py             # Root URL configuration
│   └── wsgi.py             # WSGI configuration
├── templates/              # HTML templates
│   ├── base.html           # Base template
│   └── blog/               # App-specific templates
├── static/                 # Static files (CSS, JS, images)
│   ├── css/
│   ├── js/
│   └── img/
├── media/                  # User uploaded files
├── requirements.txt        # Python dependencies
└── manage.py              # Django management script
```

## Content Management

### Admin Panel Features

- **Regions**: Manage geographical regions (Asia, Europe, Africa, etc.)
- **Categories**: Organize content by type (Main Course, Dessert, etc.)
- **Tags**: Add descriptive tags for better organization
- **Recipes**: Full recipe management with rich text editor
- **Articles**: Story and article management
- **Contact Submissions**: View user submissions

### Adding Content

1. Access admin panel at `/admin/`
2. Create regions, categories, and tags first
3. Add recipes with detailed information
4. Write articles and stories
5. Use rich text editor for formatting

## Customization

### Colors and Styling

The site uses a custom orange color scheme:
- Primary: `#ff8c00` (Orange)
- Secondary: `#ff6b35` (Red-orange)
- Custom CSS in `static/css/custom.css`

### Adding New Regions

1. Go to admin panel
2. Add new region in "Regions" section
3. Assign recipes and articles to the region

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support and questions, please contact the development team.

---

**Mesa Global** - Celebrating the world's diverse culinary traditions through food, stories, and cultural connections.