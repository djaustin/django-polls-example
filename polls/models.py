# pylint: disable=no-member
from django.db import models
from django.utils import timezone
import datetime


# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    def was_published_recently(self):
        return timezone.now() >= self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    
    def number_of_choices(self):
        return len(self.choice_set.all())

    def __str__(self):
        return self.question_text
    
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    
    def __str__(self):
        return self.choice_text