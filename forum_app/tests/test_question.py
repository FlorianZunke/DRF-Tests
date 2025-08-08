from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from forum_app.models import Question
from forum_app.api.serializers import QuestionSerializer

class QuestionTests(APITestCase):

    #Test für die GET abfrage aller Questions
    # def test_get_questions(self):
    #     url = reverse("question-list")
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)


    #Das set up für den Test, es liefert den User und die Question. 
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.question = Question.objects.create(title='Test Question', content='Test Content', author=self.user, category='frontend')

        #LogIn über die TokenAuthentication
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)  #Leerzeichen hinter dem 'Token ' nicht vergessen, sonst funktioniert es nicht

    

        #Loggt einen TestUser ein, wichtig um Permissions zu Testen(IsAutehnicated)
        # self.client = APIClient()
        # self.client.login(username='testuser', password='testpassword')


    #Test für die POST abfrage
    def test_list_post_question(self):
        url= reverse('question-list')
        data = {
            'title': 'Question',
            'content': '1Content',
            'author': self.user.id,
            'category': 'frontend'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    #Test für die Detail GET abfrage
    def test_detail_questions(self):
        url = reverse("question-detail", kwargs={'pk': self.question.id})
        response = self.client.get(url)
        excepted_data = QuestionSerializer(self.question).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.data, excepted_data)
        self.assertJSONEqual(response.content, excepted_data)

        self.assertContains(response, 'title') #kann man prüfen ob die Felder befüllt sind

        # self.assertEqual(Question.objects.count(), 1)               #Kann fehler werfen wenn die Datenbank vorher verändert
        # self.assertEqual(Question.objects.get().author, self.user)  #Kann fehler werfen wenn die Datenbank vorher verändert, kann nur 1 Question zurück geben