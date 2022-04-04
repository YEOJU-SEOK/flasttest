from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import JsonResponse 
from djangogram.users.models import User as user_model

from . import models, serializers
from .forms import CreatePostForm, CommentForm, UpdatePostForm
# Create your views here.

# db에서 포스트만 추출
    # post시리얼라이저 호출
    # return render(request, 'posts/main.html')

def index(request):
    # 로그인을 한 포스트 + 팔로잉을 한 유저의 포스트가 같이 나옴
    if request.method == "GET":
        user = get_object_or_404(user_model, pk=request.user.id)
        following = user.following.all()
        posts = models.Post.objects.filter(Q(author__in=following) | Q(author=user)).order_by("-created_at")

        serializer = serializers.PostSerializer(posts, many=True)
        form = CommentForm()
        return render(request, 'posts/main.html', {'posts': serializer.data, "comment_form": form})

def post_create(request):
    # 사용자가 페이지를 요청하는 get
    if request.method == "GET":
        form = CreatePostForm()
        return render(request, 'posts/post_create.html', {"form": form})

    elif request.method == "POST":
        # 로그인한 유저의 경우
        if request.user.is_authenticated:
            user = get_object_or_404(user_model, pk=request.user.id)
            # # 파일데이터의 경우 files, 일반 데이터의 경우 post
            # image = request.FILES['image']
            # caption = request.POST['caption']
            #
            # new_post = models.Post.objects.create(author=user, image=image, caption=caption)
            # new_post.save()
            form = CreatePostForm(request.POST, request.FILES)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = user
                post.save()
            else:
                print(form.errors)
            return redirect(reverse('posts:index'))
        else:
            return render(request, 'users/main.html')


def post_update(request, post_id):
    if request.user.is_authenticated:
        # 작성자 체크
        post = get_object_or_404(models.Post, pk=post_id)
        if request.user != post.author:
            return redirect(reverse('posts:index'))

        # GET 요청
        if request.method == 'GET':
            form = UpdatePostForm(instance=post)
            return render(
                request,
                'posts/post_update.html',
                {"form": form, "post": post}
            )

        elif request.method == 'POST':
            # 업데이트 버튼 클릭 후 저장을 위한 POST api 요청 로직
            form = UpdatePostForm(request.POST)
            if form.is_valid():
                post.caption = form.cleaned_data['caption']
                post.save()
            return redirect(reverse('posts:index'))

    else:
        return render(request, 'users/main.html')


def post_delete(request, post_id):
    if request.user.is_authenticated:
        post = get_object_or_404(models.Post, pk=post_id)
        if request.user == post.author:
            post.delete()
        return redirect(reverse('posts:index'))
    else:
        return render(request, 'users/main.html')


def comment_create(request, post_id):
    if request.user.is_authenticated:
        post = get_object_or_404(models.Post, pk=post_id)

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.posts = post
            comment.save()

            return redirect(reverse('posts:index') + "#comment-"+ str(comment.id))

        else:
            return render(request, 'users/main.html')


def comment_delete(request, comment_id):
    if request.user.is_authenticated:
        comment = get_object_or_404(models.Comment, pk=comment_id)
        if request.user == comment.author:
            comment.delete()
        return redirect(reverse('posts:index'))

    else:
        return render(request, 'users/main.html')


# 포스트 좋아요 로직
def post_like(request, post_id):
    # render할 필요가 없음
    response_body = {'result': "" }
    if request.user.is_authenticated:
        if request.method == 'POST':
            post = get_object_or_404(models.Post, pk=post_id)
            # image_likes의 경우 user필드를 조회, t/f반환
            existed_user = post.image_likes.filter(pk=request.user.id).exists()
            if existed_user:
                # 좋아요 => 취소
                post.image_likes.remove(request.user)
                response_body["result"] = "dislike"
            else:
                # 좋아요 
                post.image_likes.add(request.user)
                response_body["result"] = "like"

            post.save()

            return JsonResponse(status=200, data=response_body)  
    
    else:
        return JsonResponse(status=403, data=response_body)