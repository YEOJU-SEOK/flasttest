from django.shortcuts import render, get_object_or_404
from djangogram.users.models import User as user_model

from . import models
# Create your views here.


def index(request):

    return render(request, 'posts/base.html')


def post_create(request):
    # 사용자가 페이지를 요청하는 get
    if request.method == "GET":
        return render(request, 'posts/post_create.html')
    elif request.method == "POST":

        # 로그인한 유저의 경우
        if request.user.is_authenticated:
            user = get_object_or_404(user_model, pk=request.user.id)
            # 파일데이터의 경우 files, 일반 데이터의 경우 post
            image = request.FILES['image']
            caption = request.POST['caption']

            new_post = models.Post.objects.create(author=user, image=image, caption=caption)
            new_post.save()

            return render(request, 'posts/base.html')
        else:
            return render(request, 'users/main.html')
