# pylint: disable=no-member
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.db.models import F
from .models import Question, Choice
# Create your views here.


class IndexView(generic.ListView):
    template_name = 'index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    template_name = 'detail.html'
    model = Question

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'detail.html', {"question": question})

class ResultsView(generic.DetailView):
    template_name = 'results.html'
    model = Question

    
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'results.html', {"question": question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        try: 
            choice = question.choice_set.get(pk=request.POST["choice"])
        except (KeyError, Choice.DoesNotExist):
            return render(request, 'detail.html', {'question': question, 'error_message': 'You did not make a choice'})
        else: 
            choice.votes = F("votes") + 1
            choice.save()
            return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))