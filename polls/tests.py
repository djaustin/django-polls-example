# pylint: disable=no-member
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from .models import Question
# Create your tests here.

def create_question(question_text, days_offset):
    """
    Creates a new question with the supplied question text and a number of days offset from now.
    """
    time = timezone.now() + timezone.timedelta(days=days_offset)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionIndexViewTests(TestCase):

    def test_no_questions(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls available")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        create_question("Past question", days_offset=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "No polls available")
        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Past question>'])

    def test_future_question(self):
        create_question("Future question", days_offset=30)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls available")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        create_question("Past question.", days_offset=-30)
        create_question("Future question.", days_offset=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_two_past_questions(self):
        create_question("Past question 1.", days_offset=-30)
        create_question("Past question 2.", days_offset=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )

class QuestionResultsViewTests(TestCase):
    
    def test_new_question(self): 
        question = create_question(question_text="New question", days_offset=0)
        response = self.client.get(reverse('polls:results', args=(question.id,)))
        self.assertNotContains(response, 'votes')

class QuestionDetailViewTests(TestCase):

    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(question_text='Future question.', days_offset=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(question_text='Past Question.', days_offset=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions with a pub_date in the future.
        """
        time = timezone.now() + timezone.timedelta(days=1)
        future_question = Question(pub_date = time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions with a pub_date within the last day
        """
        time = timezone.now() - timezone.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date = time)
        self.assertIs(recent_question.was_published_recently(), True)
