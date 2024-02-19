from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from reviews.validators import validate_year

User = get_user_model()


class Genre(models.Model):
    name = models.CharField("Имя жанра", max_length=settings.MAX_LENGHT)
    slug = models.SlugField("Тег жанра", unique=True)

    class Meta:
        ordering = ("name",)
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField("Имя категории", max_length=settings.MAX_LENGHT)
    slug = models.SlugField("Тег категории", unique=True)

    class Meta:
        ordering = ("name",)
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        "Название произведения", max_length=settings.MAX_LENGHT
    )
    year = models.SmallIntegerField(
        "Год выпуска", validators=[validate_year, ]
    )
    description = models.TextField(
        "Описание", max_length=settings.MAX_LENGHT, blank=True
    )
    genre = models.ManyToManyField(Genre, verbose_name="Жанр")
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        verbose_name="Категория",
    )

    class Meta:
        ordering = ("-year",)
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"
        default_related_name = "titles"

    def __str__(self):
        return self.name


class ReviewCommentAbstractModel(models.Model):
    pub_date = models.DateTimeField("Дата добавления", auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Автор"
    )

    class Meta:
        abstract = True


class Review(ReviewCommentAbstractModel):
    text = models.TextField("Текст")
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, verbose_name="Название"
    )
    score = models.IntegerField(
        "Рейтинг",
        validators=[
            MinValueValidator(
                settings.MIN_VALIDATOR_VALUE,
                message=settings.VALUE_CANNOT_BE_LESS_THAN
            ),
            MaxValueValidator(
                settings.MAX_VALIDATOR_VALUE,
                message=settings.VALUE_CANNOT_BE_MORE_THAN),
        ],
    )

    class Meta:
        ordering = ("-pub_date",)
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        default_related_name = "reviews"
        constraints = [
            models.UniqueConstraint(
                fields=["title", "author"], name="unique_key_title_author"
            ),
        ]

    def __str__(self):
        return self.text[:settings.MAX_SLICE]


class Comment(ReviewCommentAbstractModel):
    text = models.TextField("Текст")
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Автор"
    )
    pub_date = models.DateTimeField("Дата добавления", auto_now_add=True)
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, verbose_name="Название"
    )

    class Meta:
        ordering = ("-pub_date",)
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        default_related_name = "comments"

    def __str__(self):
        return self.text[:settings.MAX_SLICE]
