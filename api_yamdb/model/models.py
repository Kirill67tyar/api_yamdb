from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Review(models.Model):
    text = models.TextField('Текст',)
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    title = models.ForeignKey(
        Titles,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Название'
    )
    rating = models.IntegerField(
        'Рейтинг',
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Comments(models.Model):
    text = models.TextField('Текст')
    created = models.DateTimeField('Дата добавления', auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    titles = models.ForeignKey(
        Titles,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Название'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
