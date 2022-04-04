from django import forms
from .models import Post, Comment


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['caption', 'image']

        labels = {'caption': "내용", "image": "사진"}


# 수정할때 이미지도 바꾼다면 CreatePostForm을 그대로 사용하면 되지만
# 수정의 경우 내용만 변경됨
class UpdatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['caption']


class CommentForm(forms.ModelForm):
    comments = forms.CharField(widget=forms.Textarea, label='')

    class Meta:
        model = Comment
        fields = ['comments']
