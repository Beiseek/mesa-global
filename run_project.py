#!/usr/bin/env python
"""
Скрипт для быстрого запуска проекта Mesa Global
"""
import os
import sys
import subprocess

def run_command(command, description):
    """Выполняет команду и выводит результат"""
    print(f"\n🚀 {description}")
    print(f"Выполняется: {command}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка: {e}")
        if e.stdout:
            print(f"Вывод: {e.stdout}")
        if e.stderr:
            print(f"Ошибки: {e.stderr}")
        return False

def main():
    print("🌍 Mesa Global - Установка и запуск проекта")
    print("=" * 50)
    
    # Проверка Python версии
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 11):
        print("❌ Требуется Python 3.11 или выше")
        print(f"Текущая версия: {python_version.major}.{python_version.minor}")
        return
    
    print(f"✅ Python версия: {python_version.major}.{python_version.minor}")
    
    # Команды для выполнения
    commands = [
        ("pip install -r requirements.txt", "Установка зависимостей"),
        ("python manage.py makemigrations", "Создание миграций"),
        ("python manage.py migrate", "Применение миграций"),
        ("python manage.py load_initial_data", "Загрузка начальных данных"),
        ("python manage.py collectstatic --noinput", "Сбор статических файлов"),
    ]
    
    # Выполнение команд
    for command, description in commands:
        if not run_command(command, description):
            print(f"\n❌ Ошибка при выполнении: {description}")
            print("Попробуйте выполнить команды вручную:")
            for cmd, desc in commands:
                print(f"  {cmd}")
            return
    
    print("\n" + "=" * 50)
    print("🎉 Проект успешно настроен!")
    print("\nДля создания администратора выполните:")
    print("  python manage.py createsuperuser")
    print("\nДля запуска сервера разработки выполните:")
    print("  python manage.py runserver")
    print("\nСайт будет доступен по адресу: http://127.0.0.1:8000/")
    print("Админ-панель: http://127.0.0.1:8000/admin/")
    print("\n🌟 Добро пожаловать в Mesa Global!")

if __name__ == "__main__":
    main()
