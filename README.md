# api_yamdb
api_yamdb

### yatube_api
yatube_api - проект, в котором можно регистрироваться, авторизовываться, писать посты, и комментарии к ним. Можно также добавлять эти посты в тематические группы, а авторизованные пользователи могут подпсываться друг на друга.
Аутентификация реализована через JWT.

### Как запустить проект:
##### Клонировать репозиторий и перейти в него в командной строке:

    git clone https://github.com/Kirill67tyar/api_final_yatube.git
    cd yatube_api

##### Cоздать и активировать виртуальное окружение:

    python3 -m venv env
- Если у вас Linux/macOS

      source env/bin/activate
	  
- Если у вас windows

      source env/scripts/activate

##### Обновляем pip
    python3 -m pip install --upgrade pip
	
##### Установить зависимости из файла requirements.txt:

    pip install -r requirements.txt
##### Выполнить миграции:

    python3 manage.py migrate
##### Запустить проект:

     python3 manage.py runserver