from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from forum_app.models import Question
from forum_app.api.serializers import QuestionSerializer

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