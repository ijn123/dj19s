# from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
# from django.template import loader
from django.core.urlresolvers import reverse
from django.db.models import F
from django.views import generic
# from django.views.generic.list import ListView
from django.utils import timezone
from .models import Choice, Question


# Create your views here.

class IndexView(generic.ListView):
# class IndexView(ListView):
    template_name = 'polls/index.html'
# default context variabl : question_list (model name + _list in this case it's question_list).That's why we use context_object_name
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        # return Question.objects.order_by('-pub_date')[:5]
        # Don't show questions in the future.
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    def get_queryset(self):
        """
        :return: the last five published questions.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def detail(request, question_id):
    # first variant using Http404 and try except
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404("Question does not exist")
    # return render(request, 'polls/detail.html', {"question":question})
    # return HttpResponse("You're looking at the results of question %s." % question_id)
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {"question": question})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question':question})
    # response = "You're looking at the results of question %s."
    # return HttpResponse(response % question_id)


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes = F('votes') + 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=[question.id]))
        # return HttpResponse("You're voting on question %s." % question_id)

# Old method isn't using now.
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:2]
    context = {
        'latest_question_list': latest_question_list,
    }
    return render(request, 'polls/index.html', context)
    # output = ', '.join([q.question_text for q in latest_question_list])
    # return HttpResponse(output)
    # second variant
    # template = loader.get_template('polls/index.html')
    # return HttpResponse(template.render(context, request))
