from django.db import models


class Genres(models.Model):
    name = models.CharField('Имя жанра', max_length=256)
    slug = models.SlugField('Тег жанра', unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Categories(models.Model):
    name = models.CharField('Имя категории', max_length=256)
    slug = models.SlugField('Тег категории', unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Titles(models.Model):
    name = models.CharField('Название произведения', max_length=256)
    year = models.IntegerField('Год выпуска')
    description = models.TextField('Описание', null=True, blank=True)
    genre = models.ManyToManyField(Genres, verbose_name='Жанр',
                                   related_name='titles')
    category = models.ForeignKey(Categories, verbose_name='Категория',
                                 on_delete=models.SET_NULL, null=True,
                                 blank=True)

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.text


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genres, on_delete=models.CASCADE)
    title = models.ForeignKey(Titles, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.genre} {self.title}'
