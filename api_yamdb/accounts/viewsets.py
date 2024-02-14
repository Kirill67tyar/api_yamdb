from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

class ListCreateModelViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    pass
