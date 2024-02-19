from datetime import timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "p&l%385148kslhtyn^##a1)ilz@4zqj=rq&agdol^##zgl9(vs"

DEBUG = True

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "django_filters",
    "rest_framework_simplejwt",
    "api.apps.ApiConfig",
    "reviews.apps.ReviewsConfig",
    "users.apps.UsersConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "api_yamdb.urls"

TEMPLATES_DIR = BASE_DIR / "templates"
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [TEMPLATES_DIR],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "api_yamdb.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = "/static/"

STATICFILES_DIRS = ((BASE_DIR / "static/"),)

AUTH_USER_MODEL = "users.User"

EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"

EMAIL_HOST_USER = "yamdb@yandex.ru"

EMAIL_FILE_PATH = BASE_DIR / "sent_emails"

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
}


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=500),
}


USER_ROLE = 'user'
MODERATOR_ROLE = 'moderator'
ADMIN_ROLE = 'admin'
MAX_LENGHT = 256
MAX_SLICE = 30
MIN_VALIDATOR_VALUE = 1
MAX_VALIDATOR_VALUE = 10
CONFIRMATION_CODE_IS_NOT_VALID = "Код подтверждения не валиден"
EMAIL_IS_NOT_UNIQUE = "Email не уникален"
USERNAME_IS_NOT_UNIQUE = "Username не уникален"
INVALID_USERNAME_FIELD_FORMAT = "Неправильный формат поля username"
THERE_IS_USER_WITH_THIS_EMAIL = (
    "Пользователь с таким email уже зарегистрирован"
)
THERE_IS_USER_WITH_THIS_USERNAME = (
    "Пользователь с таким username уже зарегистрирован"
)
MAX_LENGTH_ROLE = 25
MAX_LENGTH_EMAIL = 254
MAX_LENGTH_USERNAME = 150
EMAIL_REQUIRED = 'Email является обязательным полем'
ERROR_BAD_REQUEST = "Вы уже отправляли отзыв на это произведение"
VALUE_CANNOT_BE_LESS_THAN = "Значение не может быть меньше {value}"
VALUE_CANNOT_BE_MORE_THAN = "Значение не может быть больше {value}"
VALIDATE_YEAR_ERROR = ("{value} не может быть больше {now}")
GENRE_SHOULD_NOT_BE_EMPTY = "Жанр не должен быть пустым"
GETTING_CONFIRMATION_CODE = "Получение кода подтверждения"
USERNAME_SHOULD_NOT_HAVE_VALUE_ME = "Username не должен иметь значение 'me'"
