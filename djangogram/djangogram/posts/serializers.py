from rest_framework import serializers

from djangogram.users.models import User as user_model
from . import models

class FeedAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_model
        fields = ("id", "username", "profile_photo",)


class CommentSerializer(serializers.ModelSerializer):
    author = FeedAuthorSerializer()

    class Meta:
        model = models.Comment
        fields = ("id", "author", "comments",)


class PostSerializer(serializers.ModelSerializer):
    comment_post = CommentSerializer(many=True)
    author = FeedAuthorSerializer()

    class Meta:
        model = models.Post
        # 추출하고자 하는 필드
        fields = ("id", "image", "caption", "author", "comment_post", "image_likes", )
