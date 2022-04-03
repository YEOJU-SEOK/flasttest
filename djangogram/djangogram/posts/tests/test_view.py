from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


class TestPosts(TestCase):
    # 테스트를 위한 임시 사용자 생성(for post)
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='testaccount', email='test@test.com', password='secret')

    # get부분 테스트 코드
    def test_get_post_page(self):
        url = reverse('posts:post_create')
        response = self.client.get(url)

        # 결과값에 대한 값을 확인한다
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/post_create.html')

    # 인증, 데이터 생성에 관련된 post
    def test_create_post_page(self):
        # 로그인한 유저의 경우
        login = self.client.login(username='testaccount', password='secret')
        self.assertTrue(login)

        url = reverse('posts:post_create')
        image = SimpleUploadedFile('test.jpg', b"whatevercontents")
        response = self.client.post(url, {"image": image, "caption": 'unit_test' })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "posts/base.html")

    def test_create_post_not_login(self):
        # 로그인 하지 않은 유저가 게시글 생성할 경우
        url = reverse('posts:post_create')
        image = SimpleUploadedFile('test.jpg', b"whatevercontents")
        response = self.client.post(url, {"image": image, "caption": 'unit_test' })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/main.html")
