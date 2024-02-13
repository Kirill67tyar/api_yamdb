from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from model.models import Titles
from .permissions import IsOwnerOrReadOnly
from .serializers import CommentsSerializer, ReviewSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_title(self):
        return get_object_or_404(Titles, pk=self.kwargs.get("title_id"))

    def get_queryset(self):
        return self.get_title().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post=self.get_title())


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_title(self):
        return get_object_or_404(Titles, pk=self.kwargs.get("title_id"))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post=self.get_title())
