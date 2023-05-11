from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.db.models import F
from django.utils import timezone
from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    """def get_queryset(self):
        返回最后五个问题,包括未来的
        return Question.objects.order_by('-pub_date')[:5]"""
    def get_queryset(self):
        # 只返回当前时间之前的问题,不返回未来的问题,这里需要引入时间参数,将时间设置为现在
        # now_datetime会返回一个查询集
        # 其中包含pub_date小于或者等于timezone.now()的问题
        now_datetime = Question.objects.filter(pub_date__lte=timezone.now())
        return now_datetime.order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        # 禁止通过URL直接访问未到发布时间的问题
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

    def get_queryset(self):
        # 禁止通过URL直接访问未到发布时间问题的详情页
        return Question.objects.filter(pub_date__lte=timezone.now())


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {'question': question, 'error_message': '未选择选项', })
    else:
        selected_choice.votes = F('votes') + 1
        selected_choice.save()
        selected_choice.refresh_from_db()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
