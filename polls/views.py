# from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
# from django.template import loader
from django.core.urlresolvers import reverse
from django.db.models import F

from .models import Choice, Question


# Create your views here.
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
        return HttpResponseRedirect(reverse('polls:results', args=(question_id)))
        # return HttpResponse("You're voting on question %s." % question_id)


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:3]
    context = {
        'latest_question_list': latest_question_list,
    }
    return render(request, 'polls/index.html', context)
    # output = ', '.join([q.question_text for q in latest_question_list])
    # return HttpResponse(output)
    # second variant
    # template = loader.get_template('polls/index.html')
    # return HttpResponse(template.render(context, request))
