from rest_framework import viewsets, status
from rest_framework.parsers import (
    JSONParser,
    MultiPartParser,
    FormParser
    )
from rest_framework.response import Response
from .models import Anime
from .serializers import AnimeSerializer


class AnimeViewSet(viewsets.ModelViewSet):
    queryset = Anime.objects.all()
    serializer_class = AnimeSerializer
    parser_classes = (
        JSONParser,
        MultiPartParser,
        FormParser
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
            )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial
            )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
            )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            status=status.HTTP_204_NO_CONTENT
            )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
            )
