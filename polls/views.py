# pylint: disable=no-member
from django.shortcuts import render
from django.http import HttpResponse
from .models import Question
# Create your views here.

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    output = ''.join([f"<li>{q.question_text}</li>" for q in latest_question_list])
    return HttpResponse(f"Hello, world. You're at the polls index.\n {output}")

def detail(request, question_id):
    return HttpResponse(f"You're looking at question {question_id}")

def results(request, question_id):
    return HttpResponse(f"You're looking at the results for question {question_id}")

def vote(request, question_id):
    return HttpResponse(f"You're voting on question {question_id}")