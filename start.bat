@echo off
echo 🌍 Mesa Global - Запуск проекта
echo ================================
echo.
echo Запускаю сервер разработки...
echo.
echo Сайт будет доступен по адресу: http://127.0.0.1:8000/
echo Админ-панель: http://127.0.0.1:8000/admin/
echo.
echo Данные для входа в админку:
echo Логин: admin
echo Пароль: admin123
echo.
echo Для остановки сервера нажмите Ctrl+C
echo.
py manage.py runserver
pause
