from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from qa.models import Question
from qa.utils import paginate
from qa.forms import AnswerForm, AskForm


def test(request, *args, **kwargs):
    return HttpResponse('OK')


def question_list(request):
    qs = Question.objects.all()
    page, paginator = paginate(request, qs)
    paginator.baseurl = reverse('main') + '?page='
    context = {
        'questions': page.object_list,
        'page': page,
        'paginator': paginator,
    }
    return render(request, 'list.html', context)


def popular(request):
    qs = Question.objects.all()
    qs = qs.order_by('-rating')
    page, paginator = paginate(request, qs)
    paginator.baseurl = reverse('popular') + '?page='
    context = {
        'questions': page.object_list,
        'page': page,
        'paginator': paginator,
    }
    return render(request, 'list_rating.html', context)


def question_detail(request, id):
    question = get_object_or_404(Question, id=id)
    answers = question.answer_set.all()
    form = AnswerForm(initial={'question': str(id)})
    context = {
        'question': question,
        'answers': answers,
        'form': form,
    }
    return render(request, 'detail.html', context)


def question_ask(request):
    if request.method == 'POST':
        form = AskForm(request.POST)
        if form.is_valid():
            form._user = request.user
            ask = form.save()
            url = reverse('question_detail', args=[ask.id])
            return HttpResponseRedirect(url)
    else:
        form = AskForm()
    context = {
        'form': form
    }
    return render(request, 'ask.html', context)


def question_answer(request):
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            form._user = request.user
            answer = form.save()
            url = reverse('question_detail', args=[answer.question.id])
            return HttpResponseRedirect(url)
    return HttpResponseRedirect('/')
