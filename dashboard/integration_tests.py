from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.test.client import Client
from django.test import TestCase
from .models import *
from django.contrib.auth import authenticate
from .views import *


class Admin_Add_View_Delete_Product(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_user(
            username="admin", password="adminpass", is_staff=True, is_superuser=True,
        )
    def test_Admin_Add_View_Delete_Product(self):
        print("\ntest_Admin_Add_View_Delete_Product")
        #Admin logs in:
        self.client.login(username="admin", password="adminpass")
        #Check login successful:
        self.assertIsNotNone(authenticate(username = "admin", password = "adminpass"))
        #Check user is admin:
        self.assertTrue(self.admin.is_superuser)

        #Add data for new product:
        post_data = QueryDict(mutable=True)
        post_data["name"] = "New Product"
        post_data["category"] = "Camera"
        post_data["min_time"] = "1"
        post_data["max_time"] = "30"
        post_data["min_amount"] = "1"
        post_data["available"] = "10"
        post_data["quantity"] = "10"
        

        #Send request to add product:
        post_response = self.client.post(reverse("dashboard-products"), post_data)
        #Check request was successful:
        self.assertEqual(post_response.status_code, 302)

        #Check a product has been created:
        self.assertEquals(Product.objects.count(),1)
        
        #Check 10 (quantity provided in data) sub-products were created:
        self.assertEquals(Product_extended.objects.count(),10)

        #Check the page redirected correctly:
        self.assertRedirects(post_response, "/products/")

        #Make sure Admin sees the new product in the list:
        get_response = self.client.get(reverse("dashboard-products"))
        self.assertEqual(get_response.context["product"][0].name,"New Product")

        #View sub-products:
        get_response = self.client.get(reverse("dashboard-products-extended", kwargs={"pk": "New Product"}))
        #Check the request was succesfull:
        self.assertEqual(post_response.status_code, 302)

        #Make sure all 10 sub-products are in the list:
        self.assertEqual(get_response.context["product"][0].name, "New Product")
        self.assertEqual(get_response.context["product"][1].name, "New Product")
        self.assertEqual(get_response.context["product"][2].name, "New Product")
        self.assertEqual(get_response.context["product"][3].name, "New Product")
        self.assertEqual(get_response.context["product"][4].name, "New Product")
        self.assertEqual(get_response.context["product"][5].name, "New Product")
        self.assertEqual(get_response.context["product"][6].name, "New Product")
        self.assertEqual(get_response.context["product"][7].name, "New Product")
        self.assertEqual(get_response.context["product"][8].name, "New Product")
        self.assertEqual(get_response.context["product"][9].name, "New Product")

        #Go back to the normal products page:
        get_response = self.client.get(reverse("dashboard-products"))

        #Choose product to delete:
        get_response = self.client.get(reverse("dashboard-products-delete", kwargs={"pk": "1"}))
        
        #Make sure the right product was chosen:
        self.assertEqual(get_response.context["item"].name,"New Product")

        #Confirm deletion:
        post_response = self.client.post(reverse("dashboard-products-delete", kwargs={"pk": "1"}))

        #Make sure product was deleted:
        self.assertEquals(Product.objects.count(),0)

        #Make sure sub-products were deleted:
        self.assertEquals(Product_extended.objects.count(),0)
        
        #logout()
        self.client.logout()

class Student_Request_Admin_Approve(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_user(
            username="admin", password="adminpass", is_staff=True, is_superuser=True
        )
        self.student = User.objects.create_user(
            username="student", password="studentpass"
        )
    def test_Student_Request_Admin_Approve(self):
        print("\ntest_Student_Request_Admin_Approve")
        #Admin adds new product:
        self.client.login(username="admin", password="adminpass")
        post_data = QueryDict(mutable=True)
        post_data["name"] = "New Product"
        post_data["category"] = "Camera"
        post_data["min_time"] = "1"
        post_data["max_time"] = "30"
        post_data["min_amount"] = "1"
        post_data["available"] = "10"
        post_data["quantity"] = "10"
        post_data["photo"] = "media\media\ipad.jpg"
        post_response = self.client.post(reverse("dashboard-products"), post_data)
        self.assertEqual(post_response.status_code, 302)
        item=Product_extended.objects.get(id=1)
        item.SN="ExampleSN"
        item.save()

        #Admin logs out:
        self.client.logout()
        #Student logs in:
        self.client.login(username="student", password="studentpass")
        #Check login successful:
        self.assertIsNotNone(authenticate(username = "student", password = "studentpass"))

        #Student sees product in available product list:
        get_response = self.client.get(reverse("dashboard-index"))
        self.assertEqual(get_response.context["product"][0].name,"New Product")
        
        #Student makes a request
        post_data = QueryDict(mutable=True)
        post_data["submit_button"] = "0"
        post_data["product0"] = get_response.context["product"][0].name
        post_data["time_value"] = {5}
        post_response = self.client.post(reverse("dashboard-index"), post_data)
        
        #Make sure request was successful:
        self.assertEqual(post_response.status_code, 200)

        #Make sure a request was made:
        self.assertEqual(Request.objects.all().count(), 1)

        #Make sure student sees it in the "Existing Request" table:
        get_response=self.client.get(reverse("dashboard-index"))
        self.assertEqual(get_response.context["requests"][0].name,"New Product")

        #Student logs out:
        self.client.logout()
        #Adming logs in:
        self.client.login(username="admin", password="adminpass")
        #Check login successful:
        self.assertIsNotNone(authenticate(username = "admin", password = "adminpass"))

        #Admin clicks requests:
        get_response=self.client.get(reverse("dashboard-requests"))

        #Check Admin sees the new request:
        self.assertEqual(get_response.context["requests"][0].name,"New Product")

        #Get data from request:
        name=get_response.context["requests"][0].name
        user=get_response.context["requests"][0].username
        period=get_response.context["requests"][0].period

        post_data = QueryDict(mutable=True)
        post_data["submit_button"] = "1"
        post_data["product1"] = "ExampleSN"
        #Admin Approves new request:
        post_response=self.client.post(reverse("dashboard-request-approve", kwargs={"product": name, "user": user, "period": period}), post_data)
        
        #Make sure response was successful:
        self.assertEqual(post_response.status_code, 302)

        #Make sure the request was deleted:
        self.assertEqual(Request.objects.all().count(), 0)

        #Make sure the Order was made:
        self.assertEqual(Rented.objects.all().count(), 1)
        
        #Admin logs out:
        self.client.logout()
        #Student logs in:
        self.client.login(username="student", password="studentpass")
        #Check login successful:
        self.assertIsNotNone(authenticate(username = "student", password = "studentpass"))

        #Make sure student sees it in the "Existing Orders" table:
        get_response=self.client.get(reverse("dashboard-index"))
        self.assertEqual(get_response.context["rented"][0].name,"New Product")

        #logout()
        self.client.logout()

class Student_Reports_Faulty_Admin_Sees_Report(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_user(
            username="admin", password="adminpass", is_staff=True, is_superuser=True
        )
        self.student = User.objects.create_user(
            username="student", password="studentpass"
        )
    def test_Student_Reports_Faulty_Admin_Sees_Report(self):
        print("\ntest_Student_Reports_Faulty_Admin_Sees_Report")
        #Admin adds new product:
        self.client.login(username="admin", password="adminpass")
        post_data = QueryDict(mutable=True)
        post_data["name"] = "New Product"
        post_data["category"] = "Camera"
        post_data["min_time"] = "1"
        post_data["max_time"] = "30"
        post_data["min_amount"] = "1"
        post_data["available"] = "10"
        post_data["quantity"] = "10"
        post_data["photo"] = "media\media\ipad.jpg"
        post_response = self.client.post(reverse("dashboard-products"), post_data)
        self.assertEqual(post_response.status_code, 302)
        item=Product_extended.objects.get(id=1)
        item.SN="ExampleSN"
        item.save()
        self.client.logout()

        #Student Makes Request:
        self.client.login(username="student", password="studentpass")
        get_response = self.client.get(reverse("dashboard-index"))
        post_data = QueryDict(mutable=True)
        post_data["submit_button"] = "0"
        post_data["product0"] = get_response.context["product"][0].name
        post_data["time_value"] = {5}
        post_response = self.client.post(reverse("dashboard-index"), post_data)
        get_response=self.client.get(reverse("dashboard-index"))

        #Adming Approves Request:
        self.client.login(username="admin", password="adminpass")
        get_response=self.client.get(reverse("dashboard-requests"))
        name=get_response.context["requests"][0].name
        user=get_response.context["requests"][0].username
        period=get_response.context["requests"][0].period
        post_data = QueryDict(mutable=True)
        post_data["submit_button"] = "1"
        post_data["product1"] = "ExampleSN"
        post_response=self.client.post(reverse("dashboard-request-approve", kwargs={"product": name, "user": user, "period": period}), post_data)
        self.client.logout()
        
        #Student Reports Faulty:
        self.client.login(username="student", password="studentpass")
        post_data = QueryDict(mutable=True)
        post_data["category"] = "Other"
        post_data["fault_description"] = "Example Description"
        post_response=self.client.post(reverse("Faults", kwargs={"pk": "ExampleSN", "name": name}),post_data)

        #Make sure response was successful:
        self.assertEqual(post_response.status_code, 302)

        #Make sure item was returned:
        self.assertEqual(Rented.objects.all().count(),0)

        #Make sure Report was documented:
        self.assertEqual(Faults.objects.all().count(),1)

        #Student logs out:
        self.client.logout()

        #Admin logs in:
        self.client.login(username="admin", password="adminpass")

        #Check login successful:
        self.assertIsNotNone(authenticate(username = "admin", password = "adminpass"))

        #Admin clicks faults:
        get_response=self.client.get(reverse("dashboard-faults-show"))

        #Check Admin sees the report:
        self.assertEqual(get_response.context["faults"][0].product_name,"New Product")

        #logout()
        self.client.logout()

class Staff_Orders_Products_And_Returns_It(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_user(
            username="admin", password="adminpass", is_staff=True, is_superuser=True
        )
        self.staff = User.objects.create_user(
            username="staff", password="staffpass", is_staff=True,
        )
    def test_Staff_Orders_Products_And_Returns_It(self):
        print("\ntest_Staff_Orders_Products_And_Returns_It")
        #Admin adds new product:
        self.client.login(username="admin", password="adminpass")
        post_data = QueryDict(mutable=True)
        post_data["name"] = "New Product"
        post_data["category"] = "Camera"
        post_data["min_time"] = "1"
        post_data["max_time"] = "30"
        post_data["min_amount"] = "1"
        post_data["available"] = "10"
        post_data["quantity"] = "10"
        post_data["photo"] = "media\media\ipad.jpg"
        post_response = self.client.post(reverse("dashboard-products"), post_data)
        self.assertEqual(post_response.status_code, 302)
        item=Product_extended.objects.get(id=1)
        item.SN="ExampleSN"
        item.save()
        self.client.logout()

        #Staff Makes Request:
        self.client.login(username="staff", password="staffpass")
        get_response = self.client.get(reverse("dashboard-index"))
        post_data = QueryDict(mutable=True)
        post_data["submit_button"] = "0"
        post_data["product0"] = get_response.context["product"][0].name
        post_data["time_value"] = {5}
        post_response = self.client.post(reverse("dashboard-index"), post_data)
        get_response=self.client.get(reverse("dashboard-index"))

        #Adming Approves Request:
        self.client.login(username="admin", password="adminpass")
        get_response=self.client.get(reverse("dashboard-requests"))
        name=get_response.context["requests"][0].name
        user=get_response.context["requests"][0].username
        period=get_response.context["requests"][0].period
        post_data = QueryDict(mutable=True)
        post_data["submit_button"] = "1"
        post_data["product1"] = "ExampleSN"
        post_response=self.client.post(reverse("dashboard-request-approve", kwargs={"product": name, "user": user, "period": period}), post_data)
        self.client.logout()
        
        #Staff Product in existing Orders:
        self.client.login(username="staff", password="staffpass")
        get_response=self.client.get(reverse("dashboard-index"))
        self.assertEqual(get_response.context["rented"][0].name,"New Product")

        #Staff returns product:
        post_data = QueryDict(mutable=True)
        post_data["return_button"] = 1
        post_data["product1"] = "New Product;ExampleSN"
        post_response=self.client.post(reverse("dashboard-index"), post_data)

        #Make sure response was successful:
        self.assertEqual(post_response.status_code, 200)

        #Make sure item was returned:
        self.assertEqual(Rented.objects.all().count(),0)

        #logout()
        self.client.logout()

class Student_Asks_Question_Staff_Replies(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_user(
            username="admin", password="adminpass", is_staff=True, is_superuser=True
        )
        self.student = User.objects.create_user(
            username="student", password="studentpass"
        )
        self.staff = User.objects.create_user(
            username="staff", password="staffpass", is_staff=True,
        )
    def test_Student_Asks_Question_Staff_Replies(self):
        print("\ntest_Student_Asks_Question_Staff_Replies")
        #Admin adds new product:
        self.client.login(username="admin", password="adminpass")
        post_data = QueryDict(mutable=True)
        post_data["name"] = "New Product"
        post_data["category"] = "Camera"
        post_data["min_time"] = "1"
        post_data["max_time"] = "30"
        post_data["min_amount"] = "1"
        post_data["available"] = "10"
        post_data["quantity"] = "10"
        post_data["photo"] = "media\media\ipad.jpg"
        post_response = self.client.post(reverse("dashboard-products"), post_data)
        self.assertEqual(post_response.status_code, 302)
        item=Product_extended.objects.get(id=1)
        item.SN="ExampleSN"
        item.save()
        self.client.logout()

        #Student Makes Request:
        self.client.login(username="student", password="studentpass")
        get_response = self.client.get(reverse("dashboard-index"))
        post_data = QueryDict(mutable=True)
        post_data["submit_button"] = "0"
        post_data["product0"] = get_response.context["product"][0].name
        post_data["time_value"] = {5}
        post_response = self.client.post(reverse("dashboard-index"), post_data)
        get_response=self.client.get(reverse("dashboard-index"))

        #Adming Approves Request:
        self.client.login(username="admin", password="adminpass")
        get_response=self.client.get(reverse("dashboard-requests"))
        name=get_response.context["requests"][0].name
        user=get_response.context["requests"][0].username
        period=get_response.context["requests"][0].period
        post_data = QueryDict(mutable=True)
        post_data["submit_button"] = "1"
        post_data["product1"] = "ExampleSN"
        post_response=self.client.post(reverse("dashboard-request-approve", kwargs={"product": name, "user": user, "period": period}), post_data)
        self.client.logout()
        
        #Student Asks Question:
        self.client.login(username="student", password="studentpass")
        post_data = QueryDict(mutable=True)
        post_data["send_question_button"] = 1
        post_data["question"] = "Example Question"
        post_response=self.client.post(reverse("dashboard-question-answer", kwargs={"rented": name, "rentedSN": "ExampleSN"}),post_data)

        #Make sure response was successful:
        self.assertEqual(post_response.status_code, 200)

        #Make sure question was saved:
        self.assertEqual(Rented.objects.get(name= name).question, "Example Question")

        #Student logs out:
        self.client.logout()

        #Staff logs in:
        self.client.login(username="staff", password="staffpass")

        #Check login successful:
        self.assertIsNotNone(authenticate(username = "staff", password = "staffpass"))

        #Check Staff sees question:
        get_response=self.client.get(reverse("dashboard-index"))
        self.assertEqual(get_response.context["rented"][0].question,"Example Question")
        
        #Staff answers question:
        post_data = QueryDict(mutable=True)
        post_data["send_answer_button"] = 1
        post_data["answer"] = "Example Answer"
        post_response=self.client.post(reverse("dashboard-question-answer", kwargs={"rented": name, "rentedSN": "ExampleSN"}),post_data)

        #Make sure response was successful:
        self.assertEqual(post_response.status_code, 200)

        #Make sure answer was saved:
        self.assertEqual(Rented.objects.get(name= name).answer, "Example Answer")

        #Staff logs out:
        self.client.logout()

        #Student logs in:
        self.client.login(username="student", password="studentpass")

        #Check login successful:
        self.assertIsNotNone(authenticate(username = "student", password = "studentpass"))
        
        #Check student sees answer:
        get_response=self.client.get(reverse("dashboard-index"))
        self.assertEqual(get_response.context["rented"][0].answer,"Example Answer")        

        #logout()
        self.client.logout()


class Staff_Requests_Stock_Admin_Sees_Request_And_Closes_It(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_user(
            username="admin", password="adminpass", is_staff=True, is_superuser=True
        )
        self.staff = User.objects.create_user(
            username="staff", password="staffpass", is_staff=True,
        )
    def test_Staff_Requests_Stock_Admin_Sees_Request_And_Closes_It(self):
        print("\ntest_Staff_Requests_Stock_Admin_Sees_Request_And_Closes_It")
        #Admin adds new product:
        self.client.login(username="admin", password="adminpass")
        post_data = QueryDict(mutable=True)
        post_data["name"] = "New Product"
        post_data["category"] = "Camera"
        post_data["min_time"] = "1"
        post_data["max_time"] = "30"
        post_data["min_amount"] = "1"
        post_data["available"] = "10"
        post_data["quantity"] = "10"
        post_data["photo"] = "media\media\ipad.jpg"
        post_response = self.client.post(reverse("dashboard-products"), post_data)
        self.assertEqual(post_response.status_code, 302)
        item=Product_extended.objects.get(id=1)
        item.SN="ExampleSN"
        item.save()
        self.client.logout()

        #Staff Logs in:
        self.client.login(username="staff", password="staffpass")

        #Check login successful:
        self.assertIsNotNone(authenticate(username = "staff", password = "staffpass"))

        #Staff home page
        get_response = self.client.get(reverse("dashboard-index"))

        #Staff Asks for More Stock:
        post_data = QueryDict(mutable=True)
        post_data["amount_needed"] = 20
        post_response = self.client.post(reverse("request-more", kwargs={"name": "New Product"}), post_data)

        #Make sure response was successful:
        self.assertEqual(post_response.status_code, 302)

        #Make sure the Stock Request was made:
        self.assertEqual(Stock_request.objects.all().count(), 1)

        #Staff Logs Out:
        self.client.logout()
        
        #Admin logs in:
        self.client.login(username="admin", password="adminpass")
        
        #Check login successful:
        self.assertIsNotNone(authenticate(username = "admin", password = "adminpass"))
        
        #Admin Clicks Stock Requests:
        get_response = self.client.get(reverse("stock-requests-show"))

        #Check Admin Sees Stock Request:
        self.assertEqual(get_response.context["stock"][0].name,"New Product")

        #Admin Closes The Request:
        post_response = self.client.post(reverse("deny-stock-request", kwargs={"product": "New Product" , "quantity": 20}), post_data)

        #Make sure response was successful:
        self.assertEqual(post_response.status_code, 302)

        #Make sure the Stock Request was closed:
        self.assertEqual(Stock_request.objects.all().count(), 0)
        
        #logout()
        self.client.logout()

class Staff_Reserves_For_Himself_And_For_Students(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_user(
            username="admin", password="adminpass", is_staff=True, is_superuser=True
        )
        self.staff = User.objects.create_user(
            username="staff", password="staffpass", is_staff=True,
        )
        self.student = User.objects.create_user(
            username="student", password="studentpass"
        )
    def test_Staff_Reserves_For_Himself_And_For_Students(self):
        print("\ntest_Staff_Reserves_For_Himself_And_For_Students")
        #Admin adds new product:
        self.client.login(username="admin", password="adminpass")
        post_data = QueryDict(mutable=True)
        post_data["name"] = "New Product"
        post_data["category"] = "Camera"
        post_data["min_time"] = "1"
        post_data["max_time"] = "30"
        post_data["min_amount"] = "1"
        post_data["available"] = "10"
        post_data["quantity"] = "10"
        post_data["photo"] = "media\media\ipad.jpg"
        post_response = self.client.post(reverse("dashboard-products"), post_data)
        self.assertEqual(post_response.status_code, 302)
        item=Product_extended.objects.get(id=1)
        item.SN="ExampleSN"
        item.save()
        item=Product_extended.objects.get(id=2)
        item.SN="ExampleSN2"
        item.save()
        self.client.logout()

        #Staff logs in:
        self.client.login(username="staff", password="staffpass")

        #Check login successful:
        self.assertIsNotNone(authenticate(username = "staff", password = "staffpass"))

        #Staff home page
        get_response = self.client.get(reverse("dashboard-index"))

        #Staff Reserves for himself:
        post_data = QueryDict(mutable=True)
        post_data["submit_button"] = 1
        post_data["product1"] = "ExampleSN"
        post_data["product2"] = "ExampleSN2"
        post_response = self.client.post(reverse("dashboard-staff-reserve", kwargs={"product": "New Product"}), post_data)

        #Make sure response was successful:
        self.assertEqual(post_response.status_code, 302)

        #Make sure the item was reserved:
        self.assertEqual(Product_extended.objects.filter(name="New Product", SN="ExampleSN")[0].status, "Reserved: staff")

        #Staff Reserves for student:
        post_data = QueryDict(mutable=True)
        post_data["amount_needed"] = 1
        post_data["under_button"] = 1
        post_data["product1"] = "ExampleSN"
        post_data["product2"] = "ExampleSN2"
        post_response = self.client.post(reverse("dashboard-staff-reserve-students", kwargs={"product": "New Product"}), post_data)

        #Make sure response was successful:
        self.assertEqual(post_response.status_code, 302)

        #Make sure the item was reserved:
        self.assertEqual(Product_extended.objects.filter(name="New Product", SN="ExampleSN2")[0].status, "Reserved")

        #logout()
        self.client.logout()

