# 🚀 Инструкции по развертыванию Mesa Global

## 📋 Шаг 1: Создание репозитория на GitHub

1. **Войдите в GitHub** под пользователем `beiseek`
2. **Создайте новый репозиторий:**
   - Название: `mesa-global`
   - Описание: `Multicultural Gastronomic Blog - Django Website`
   - Публичный репозиторий
   - НЕ добавляйте README, .gitignore или лицензию (они уже есть)

3. **После создания репозитория выполните:**
   ```bash
   git push -u origin main
   ```

## 🖥️ Шаг 2: Развертывание на сервере

### Подключение к серверу:
```bash
ssh root@62.60.157.18
# Пароль: 22pw8bwsKGN3
```

### Автоматическое развертывание:
```bash
# Скачайте и запустите скрипт развертывания
wget https://raw.githubusercontent.com/beiseek/mesa-global/main/deploy.sh
chmod +x deploy.sh
./deploy.sh
```

### Ручное развертывание (если нужно):

1. **Обновите систему:**
   ```bash
   apt update && apt upgrade -y
   ```

2. **Установите зависимости:**
   ```bash
   apt install -y python3-pip python3-venv python3-dev nginx postgresql postgresql-contrib libpq-dev
   ```

3. **Создайте директорию проекта:**
   ```bash
   mkdir -p /var/www/mesa-global
   cd /var/www/mesa-global
   ```

4. **Клонируйте репозиторий:**
   ```bash
   git clone https://github.com/beiseek/mesa-global.git .
   ```

5. **Настройте виртуальное окружение:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

6. **Настройте базу данных:**
   ```bash
   sudo -u postgres psql -c "CREATE DATABASE mesa_global;"
   sudo -u postgres psql -c "CREATE USER mesa_user WITH PASSWORD 'mesa_global_2024';"
   sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE mesa_global TO mesa_user;"
   ```

7. **Настройте Django для продакшена:**
   ```bash
   export DJANGO_SETTINGS_MODULE=mesa_global.settings_production
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py load_initial_data
   python manage.py collectstatic --noinput
   ```

8. **Настройте Gunicorn и Nginx:**
   ```bash
   # Запустите скрипт развертывания для автоматической настройки
   ./deploy.sh
   ```

## 🔧 Управление проектом

### Полезные команды:

```bash
# Проверить статус сервиса
sudo systemctl status mesa-global

# Перезапустить сервис
sudo systemctl restart mesa-global

# Посмотреть логи
sudo journalctl -u mesa-global -f

# Обновить проект
cd /var/www/mesa-global
git pull origin main
sudo systemctl restart mesa-global
```

### Обновление проекта:
```bash
cd /var/www/mesa-global
./update.sh
```

## 🌐 Доступ к сайту

После успешного развертывания:
- **Основной сайт:** http://62.60.157.18
- **Админ-панель:** http://62.60.157.18/admin

## 🔐 Безопасность

1. **Измените пароль базы данных** в настройках продакшена
2. **Настройте SSL сертификат** для HTTPS
3. **Настройте файрвол** для ограничения доступа
4. **Регулярно обновляйте** систему и зависимости

## 📞 Поддержка

При возникновении проблем:
1. Проверьте логи: `sudo journalctl -u mesa-global -f`
2. Проверьте статус сервисов: `sudo systemctl status mesa-global nginx`
3. Проверьте конфигурацию Nginx: `sudo nginx -t`

---

**Удачного развертывания! 🎉**
