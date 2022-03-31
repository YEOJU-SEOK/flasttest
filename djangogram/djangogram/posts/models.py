from django.db import models
from djangogram.users import models as user_model

# Create your models here.
# created, updated날짜를 사용하므로 이를 상속해서 사용하게 함


class TimeStamedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# 포스트 관리db
class Post(TimeStamedModel):
    author = models.ForeignKey(user_model.User, null=True, on_delete=models.CASCADE, related_name='comment_author')
    image = models.ImageField(blank=True)
    caption = models.TextField(blank=True)
    image_likes = models.ManyToManyField(user_model.User, related_name='post_like')


# 댓글 관리db
class Comment(TimeStamedModel):
    author = models.ForeignKey(user_model.User, null=True, on_delete=models.CASCADE, related_name='post_author')
    posts = models.ForeignKey(Post, null=True, on_delete=models.CASCADE, related_name='comment_post')
    comments = models.TextField(blank=True)
