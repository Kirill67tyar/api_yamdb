## API_YaMDb
 
API_YaMDb - проект, в котором можно можно оставлять отзывы на произведения в различных категориях, ставить оценки и оставлять комментарии к отзывам. 
Аутентификация реализована через JWT.

### Как запустить проект:

##### Клонировать репозиторий и перейти в него в командной строке:
```
git@github.com:Kirill67tyar/api_yamdb.git
```

```
cd api_yamdb/
```
 
##### Cоздать и активировать виртуальное окружение:
```
python3 -m venv env
```

```
- Если у вас Linux/macOS:
 
    source env/bin/activate
     
- Если у вас windows:
 
    source env/scripts/activate
```
 
##### Обновить pip
```
python3 -m pip install --upgrade pip
```
   
##### Установить зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```

##### Выполнить миграции:
```
python3 manage.py migrate
```

##### Запустить проект:
```
python3 manage.py runserver
```

### Документация к API:
```
Документация к API доступна по адресу: http://127.0.0.1:8000/redoc/
```

### Примеры запросов

##### Получение списка всех произведений:
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

##### Получение списка всех отзывов:
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

##### Получение комментария к отзыву:
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

##### Добавление пользователя:
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