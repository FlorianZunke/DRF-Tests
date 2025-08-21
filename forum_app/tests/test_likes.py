from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from forum_app.models import Question, Like
from forum_app.api.serializers import QuestionSerializer, LikeSerializer

#Test wird gestartet mit python manage.py test

#Es wird eine Datenbank kopie angelegt und getestet, deswegen muss man Set ups anlegen für ManyToMany realtionen
#Die Datenbankkopie wird danach wieder gelöscht

#Es werden nur funktion die Test am anfang stehen haben als Test gezählt.

class LikeTests(APITestCase):
    #Test für die GET abfrage aller likes
    def test_get_like(self):
        url = reverse("like-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.question = Question.objects.create(title='Test Question', content='Test Content', author=self.user, category='frontend')

        # LogIn über die TokenAuthentication
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)



    def test_post_like(self):
        url = reverse('like-list')
        data = {
            'question': self.question.id
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Like.objects.filter(user=self.user, question=self.question).exists())


    def test_get_like_detail(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.question = Question.objects.create(title='Test Question', content='Test Content', author=self.user, category='frontend')
        # Erstelle einen Like für den Test
        self.like = Like.objects.create(user=self.user, question=self.question)
        
        # LogIn über die TokenAuthentication
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        url = reverse("like-detail", kwargs={'pk': self.like.id})
        response = self.client.get(url)
        expected_data = LikeSerializer(self.like).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.data, expected_data)
        self.assertJSONEqual(response.content, expected_data)