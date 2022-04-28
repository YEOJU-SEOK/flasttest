from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Question, Choice


# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     context = {
#         'latest_question_list' : latest_question_list,
#     }
#     # 동일한 기능 단축키로 render() 제공
#     # return HttpResponse(template.render(context, request))
#     # 인수 ; request, 탬플릿 이름, context(사전형)객체(optional)
#     return render(request, 'polls/index.html', context)


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    # context_object_name : 기본적으로 장고는 object_list라는 변수에 해당 객체를 담는다, 뷰에서 템플릿 파일에 전달하는 컨텍스트 변수명을 지정한다.
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        # 가장 최근의 5개의 질문 리턴
        # return Question.objects.order_by('-pub_date')[:5]
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5] # test

# def detail(request, question_id):
#     # try:
#     #     question = Question.objects.get(pk=question_id)
#     # except Question.DoesNotExist:
#     #     raise Http404("Question does not exist")
#
#     # 단축키 get_object_or_404()
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/detail.html', {'question': question})


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """ 아직 발행되지 않은 값은 반환되지 않게
        (미래시점으로 등록한 설문은 실제로 보이지 않으나 url 노출 가능성이 있으므로 이를 수정해줌)"""
        return Question.objects.filter(pub_date__lte=timezone.now()) # test

# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {"question": question})


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        # request.POST 는 키로 전송된 자료에 접근할 수 있도록 해주는 사전과 같은 객체
        # request.POST['choice']는 선택된 설문의 ID를 문자열로 반환
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {'question': question,
                                                     "error_message": "You didn't select a choice.", })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # 302 리다이렉트를 위해 아래 로직 사용 => /polls/3/results/반환해줌
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))