import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """ was_published_recently() return 'false'
            for questions whose pub_date(future)"""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)

        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """ was_published_recently() return 'false'
                    for questions whose pub_date(older than 1day)"""
        time = timezone.now() - datetime.timedelta(days=1)
        old_question = Question(pub_date=time)

        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """ was_published_recently() return 'true'
                    for questions whose pub_date(last day)"""
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)

        self.assertIs(recent_question.was_published_recently(), True)


# IndexView test
def create_question(question_text, days):
    """ 질문 등록날짜가 공개된건 음수, 공개되지 않은건 양수임"""
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):
    def test_no_question(self):
        """ 질문이 존재하지 않을경우, 적절한 메세지가 반환"""
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available")

        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """ 과거날짜의 질문들이 인덱스페이지에 표시됨 """
        question = create_question(question_text="Past question", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [question])

    def test_future_question(self):
        """ 미래날짜로 등록한 질문들이 인덱스페이지에 표시되는지 """
        question = create_question(question_text="future question", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_two_past_question(self):
        """하나의 인덱스페이지에 나오는 결과값이 복수인지 확인"""
        question1 = create_question(question_text="past question1", days=-30)
        question2 = create_question(question_text="past question2", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [question2, question1])


# DetailView Test

class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """ 미래 날짜 설문 호출시 404에러"""
        future_question = create_question(question_text='future question', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """ 과거 날짜 설문 호출시 해당 설문 보여줌 """
        past_question = create_question(question_text='past question', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
