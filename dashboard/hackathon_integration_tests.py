from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.test.client import Client
from django.test import TestCase
from .models import *
from django.contrib.auth import authenticate
from .views import *


class Admin_chat_with_Student(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_user(
            username="admin", password="adminpass", is_staff=True, is_superuser=True
        )
        self.student = User.objects.create_user(
            username="student", password="studentpass"
        )
    def test_Admin_chat_with_Student(self):
        print("\ntest_Admin_chat_with_Student")

        #Admin logs in:
        self.client.login(username="admin", password="adminpass")
        #Check login successful:
        self.assertIsNotNone(authenticate(username = "admin", password = "adminpass"))
        #Check user is admin:
        self.assertTrue(self.admin.is_superuser)

        #Admin goes to chat page:
        get_response = self.client.get(reverse("dashboard-chat"))

        #Admin opens a new chat:
        post_data = QueryDict(mutable=True)
        post_data["new_chat_button"] = "0"
        post_data["chat0"] = "student"
        post_response = self.client.post(reverse("dashboard-chat"), post_data)
        
        #Check response was successful:
        self.assertEqual(post_response.status_code, 302)

        #Admin sees the new chat:
        get_response = self.client.get(reverse("dashboard-chat-open", kwargs={"sender": "admin"}))

        #Admin sends a message:
        post_data = QueryDict(mutable=True)
        post_data["message"] = "example message admin to student"
        post_response = self.client.post(reverse("dashboard-chat-open", kwargs={"sender": "admin"}), post_data)

        #Check response was successful:
        self.assertEqual(post_response.status_code, 200)

        #Check a message was created:
        self.assertEqual(Message.objects.all().count(),1)

        #Admin logs out:
        self.client.logout()
        
        #Student logs in:
        self.client.login(username="student", password="studentpass")
        #Check login successful:
        self.assertIsNotNone(authenticate(username = "student", password = "studentpass"))

        #Student goes to chat:
        get_response = self.client.get(reverse("dashboard-chat"))

        #Student opens chat:
        get_response = self.client.get(reverse("dashboard-chat-open", kwargs={"sender": "admin"}))

        #Make sure the student sees the new message:
        self.assertEqual(Message.objects.get(sender = "admin").content, "example message admin to student")
        
        #Student answers on the message:
        post_data = QueryDict(mutable=True)
        post_data["message"] = "example answer student to admin"
        post_response = self.client.post(reverse("dashboard-chat-open", kwargs={"sender": "student"}), post_data)

        #Check response was successful:
        self.assertEqual(post_response.status_code, 200)

        #Check a message was created:
        self.assertEqual(Message.objects.all().count(),2)

        #Student logs out:
        self.client.logout()
        
        #Admin logs in:
        self.client.login(username="admin", password="adminpass")
        #Check login successful:
        self.assertIsNotNone(authenticate(username = "admin", password = "adminpass"))
        #Check user is admin:
        self.assertTrue(self.admin.is_superuser)

        #Admin opens chat:
        get_response = self.client.get(reverse("dashboard-chat-open", kwargs={"sender": "student"}))
        
        #Make sure the admin sees the new message:
        self.assertEqual(Message.objects.get(sender = "student").content, "example answer student to admin")


        #logout
        self.client.logout()
