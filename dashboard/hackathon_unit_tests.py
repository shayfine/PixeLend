from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.test.client import Client
from django.test import TestCase
from .models import *
from django.contrib.auth import authenticate
from .views import *


class Test_Chat_Page(TestCase):
    def test_chat_page(self):
        url = reverse("dashboard-chat")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

class Test_Chat_Show_Page(TestCase):
    def test_chat_show(self):
        sender = "shayfine"
        url = reverse("dashboard-chat-open", kwargs={"sender": sender})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)