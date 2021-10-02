# Реализация сервиса сканирования локальной сети
## Само задание
Написать сервис на Django + Celery + MongoDB + Redis + REST API, выполняющий сканирование локальной сети с помощью nmap. Результат должен быть преобразован в json и сохранен в БД.

# Установка и запуск
На данной ветке не использован докер
## Установка основых компонентов
Скопируйте репозиторий

Установите Python версии 3.9.7

https://www.python.org/downloads/

Создайте виртуальное окружение и активируйте его

https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/26/python-virtual-env/

Перейдите в директорию проекта и установите необходимые пакеты
```
pip install -r requirements.txt
```
Установите и запустите MongoDB, Redis, Nmap
- Mongo https://docs.mongodb.com/manual/administration/install-community/
- Redis https://redis.io/topics/quickstart
- Nmap https://nmap.org/download.html

Перейдите в основную папку проекта, та директория, что содержит файл `manage.py`

В данной директории создайте файл .env, скопируйте содержимое из .env и наполните его необходимыми значениями

## Запуск сервиса
После установки всех пакетов и настрйоки проекта

Создайте суперпользователя
```
python manage.py createsuperuser
```
Запустите миграции
```
python manage.py migrate
```
Запустите встроенный сервер Django
```
python manage.py runserver
```
