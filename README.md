## API_YaMDb
 
API_YaMDb - проект, в котором можно можно оставлять отзывы на произведения в различных категориях, ставить оценки и оставлять комментарии к отзывам. 
Аутентификация реализована через JWT.

### Как запустить проект:

```
1. Клонировать репозиторий и перейти в него в командной строке:

   git@github.com:Kirill67tyar/api_yamdb.git
   
   cd api_yamdb/

2. Cоздать и активировать виртуальное окружение:

   python3 -m venv env

-  Если у вас Linux/macOS:
 
   source env/bin/activate
     
-  Если у вас windows:
 
   source env/scripts/activate

3. Обновить pip

   python3 -m pip install --upgrade pip

4. Установить зависимости из файла requirements.txt:

   pip install -r requirements.txt

5. Выполнить миграции:

   python3 manage.py migrate

6. Запустить проект:

   python3 manage.py runserver
```

### Документация к API:
```
Документация к API доступна по адресу: http://127.0.0.1:8000/redoc/
```

### Примеры запросов:

##### Получить список всех произведений:
```
Request: [GET] http://127.0.0.1:8000/api/v1/titles/
```

```
Response samples:
```

```
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "id": 0,
      "name": "string",
      "year": 0,
      "rating": 0,
      "description": "string",
      "genre": [
        {
          "name": "string",
          "slug": "string"
        }
      ],
      "category": {
        "name": "string",
        "slug": "string"
      }
    }
  ]
}
```

##### Получить список всех отзывов:
```
Request: [GET] http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/
```

```
Response samples:
```

```
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "id": 0,
      "text": "string",
      "author": "string",
      "score": 1,
      "pub_date": "2019-08-24T14:15:22Z"
    }
  ]
}
```

##### Получить комментарий к отзыву:
```
Request: [GET] http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
```

```
Response samples:
```

```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "pub_date": "2019-08-24T14:15:22Z"
}
```

##### Добавить пользователя:
```
Request: [GET] http://127.0.0.1:8000/api/v1/users/
```

```
Response samples:
```

```
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```

### Как наполнить базу:

```
1. Перейти в дирректорию с csv файлами.
   Убедиться, что CSV-файл содержит корректные данные с заголовками, соответствующими столбцам в вашей таблице базы данных.

2. Открыть SQLite Shell:
   В командной строке ввести команду для открытия SQLite Shell указывая путь к библиотеке:
   sqlite3 ../../db.sqlite3

3. Указать режим CSV:
   .mode csv

4. Настроить разделитель:
   .separator ","

5. Импортировать данные.
   Использовать команду .import для импорта данных из CSV-файла, где 'file'.csv - имя вашего CSV-файла, а 'table_name' - имя таблицы в базе данных, куда вы хотите импортировать данные.
   .import category.csv reviews_category
   .import comments.csv reviews_comment
   .import genre.csv reviews_genre
   .import review.csv reviews_review
   .import titles.csv reviews_title
   .import users.csv users_user

6. Проверить результат.
   Выйти из SQLite Shell:
   .quit
```
