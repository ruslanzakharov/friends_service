# friends_service
Сервис, который реализует функционал работы с друзьями в социальных сетях

### Запуск

1. Склонировать репозиторий
```commandline
git clone https://github.com/ruslanzakharov/friends_service.git
```
2. Установить poetry
```commandline
pip install poetry
```
3. В корне склонированного проекта создать виртуальное окружение с установленными зависимостями
```commandline
poetry install
```
4. Активировать виртуальное окружение
```commandline
poetry shell
```
5. Создать миграции и применить их
```commandline
python manage.py makemigrations
python manage.py migrate
```
6. Запустить сервис
```commandline
python manage.py runserver
```

### Использование

- Обращаться к API через URL `http://127.0.0.1:8000`
- Доступные к вызову методы описаны в OpenAPI спецификации в файле openapi.yaml
