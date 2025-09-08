# 🚀 Быстрое развертывание Mesa Global

## 📋 Что нужно сделать:

### 1. Создать репозиторий на GitHub
1. Зайдите на https://github.com/beiseek
2. Нажмите "New repository"
3. Название: `mesa-global`
4. Описание: `Multicultural Gastronomic Blog - Django Website`
5. Публичный репозиторий
6. НЕ добавляйте README, .gitignore или лицензию
7. Нажмите "Create repository"

### 2. Загрузить код на GitHub
После создания репозитория выполните:
```bash
git push -u origin main
```

### 3. Развернуть на сервере
Подключитесь к серверу:
```bash
ssh root@62.60.157.18
# Пароль: 22pw8bwsKGN3
```

На сервере выполните:
```bash
# Обновить систему
apt update && apt upgrade -y

# Установить зависимости
apt install -y python3-pip python3-venv python3-dev nginx postgresql postgresql-contrib libpq-dev git

# Создать директорию проекта
mkdir -p /var/www/mesa-global
cd /var/www/mesa-global

# Клонировать репозиторий
git clone https://github.com/beiseek/mesa-global.git .

# Создать виртуальное окружение
python3 -m venv venv
source venv/bin/activate

# Установить зависимости
pip install -r requirements.txt

# Настроить базу данных
sudo -u postgres psql -c "CREATE DATABASE mesa_global;"
sudo -u postgres psql -c "CREATE USER mesa_user WITH PASSWORD 'mesa_global_2024';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE mesa_global TO mesa_user;"

# Создать настройки для продакшена
cat > mesa_global/settings_production.py << 'EOF'
from .settings import *
import os

DEBUG = False
ALLOWED_HOSTS = ['62.60.157.18', 'localhost', '127.0.0.1']

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

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
EOF

# Запустить миграции
export DJANGO_SETTINGS_MODULE=mesa_global.settings_production
python manage.py migrate

# Создать суперпользователя
python manage.py createsuperuser

# Загрузить начальные данные
python manage.py load_initial_data

# Собрать статические файлы
python manage.py collectstatic --noinput

# Настроить Gunicorn
cat > /etc/systemd/system/mesa-global.service << 'EOF'
[Unit]
Description=Mesa Global Django App
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=/var/www/mesa-global
Environment="PATH=/var/www/mesa-global/venv/bin"
Environment="DJANGO_SETTINGS_MODULE=mesa_global.settings_production"
ExecStart=/var/www/mesa-global/venv/bin/gunicorn --workers 3 --bind unix:/var/www/mesa-global/mesa-global.sock mesa_global.wsgi:application
ExecReload=/bin/kill -s HUP $MAINPID
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF

# Настроить Nginx
cat > /etc/nginx/sites-available/mesa-global << 'EOF'
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

# Включить сайт
ln -s /etc/nginx/sites-available/mesa-global /etc/nginx/sites-enabled
rm -f /etc/nginx/sites-enabled/default

# Проверить конфигурацию
nginx -t

# Запустить сервисы
systemctl daemon-reload
systemctl start mesa-global
systemctl enable mesa-global
systemctl restart nginx

# Установить права
chown -R root:www-data /var/www/mesa-global
chmod -R 755 /var/www/mesa-global

echo "✅ Развертывание завершено!"
echo "🌐 Сайт доступен по адресу: http://62.60.157.18"
echo "👤 Админ-панель: http://62.60.157.18/admin"
```

## 🔧 Управление после развертывания:

```bash
# Проверить статус
systemctl status mesa-global

# Перезапустить
systemctl restart mesa-global

# Посмотреть логи
journalctl -u mesa-global -f

# Обновить код
cd /var/www/mesa-global
git pull origin main
systemctl restart mesa-global
```

## 🌐 Результат:
- **Сайт:** http://62.60.157.18
- **Админ:** http://62.60.157.18/admin
- **GitHub:** https://github.com/beiseek/mesa-global
