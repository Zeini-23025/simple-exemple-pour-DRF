from rest_framework import serializers

from .models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post

        fields = [
            "id", "title",
            "content", "created_at",
            "updated_at"
            ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at"
            ]

        extra_kwargs = {
            "title": {
                "required": True,
                "max_length": 200
                },
            "content": {
                "required": True
                },
        }
