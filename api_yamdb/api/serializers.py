from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from model.models import (
  Categories,
  Genres,
  Titles,
  Comments,
  Review
                         )


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ('id', )
        model = Categories
        lookup_field = 'slug'


class GenresSerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ('id', )
        model = Genres
        lookup_field = 'slug'


class TitlesReadSerializer(serializers.ModelSerializer):
    category = CategoriesSerializer(read_only=True)
    genre = GenresSerializer(
        read_only=True,
        many=True
    )
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Titles


class TitlesWriteSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Categories.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genres.objects.all(),
        slug_field='slug',
        many=True
    )

    class Meta:
        fields = '__all__'
        model = Titles
        

class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('title',)


class CommentsSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Comments
        fields = '__all__'
        read_only_fields = ('title',)
