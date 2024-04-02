from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.test.client import Client
from django.test import TestCase
from .models import *
from django.contrib.auth import authenticate
from .views import *


class Test_site_works(TestCase):
    def test_site_is_up(self):
        url = reverse("dashboard-index")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)


class LoginTestCase(TestCase):
    def test_login_fails(self):
        self.assertIsNone(authenticate(username = "wrong_username", password = "wrong_password"))

    def test_login_success(self):
        User.objects.create_user("username", "email", "password")
        self.assertIsNotNone(authenticate(username = "username", password = "password"))

class AdminPrivilegeTestCase(TestCase):
    def test_admin_has_privilege(self):
        self.client.login(username="shayfine", password="1234")
        response = self.client.get(reverse("dashboard-products"))
        self.assertEqual(response.status_code, 302)

    def test_user_does_not_have_privilege(self):
        self.client.login(username="guy", password="gguuyygguuyy")
        response = self.client.get(reverse("dashboard-products"))
        self.assertEqual(response.status_code, 302)


class DashboardViewsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.product = Product.objects.create(
            name="Test Product",
            quantity=10,
            category="Camera",
            min_time=1,
            max_time=10,
            min_amount=1,
        )
        self.product_extended = Product_extended.objects.create(
            name="Test Product Extended",
            SN="1234567890",
            status="available",
            faulty="NO",
        )
        self.order = Order.objects.create(
            name=self.product, customer=self.user, order_quantity=2
        )

    def test_product_detail_view(self):
        url = reverse("dashboard-products-detail", kwargs={"pk": self.product.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_product_edit_view(self):
        url = reverse("dashboard-products-edit", kwargs={"pk": self.product.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_product_delete_view(self):
        url = reverse("dashboard-products-delete", kwargs={"pk": self.product.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Product.objects.filter(pk=self.product.pk).exists())

    def test_product_extended_edit_view(self):
        url = reverse(
            "dashboard-products-extended-edit", kwargs={"pk": self.product_extended.pk}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_customers_view(self):
        url = reverse("dashboard-customers")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_customer_detail_view(self):
        url = reverse("dashboard-customer-detail", kwargs={"pk": self.user.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_order_view(self):
        url = reverse("dashboard-order")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_product_extended_view(self):
        url = reverse(
            "dashboard-products-extended", kwargs={"pk": self.product_extended.pk}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)


class ProductDetailViewTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Test Product",
            quantity=10,
            category="Camera",
            min_time=1,
            max_time=5,
            min_amount=1,
        )
        self.url = reverse("dashboard-products-detail", args=[self.product.id])

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)


class ProductEditViewTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Test Product",
            quantity=10,
            category="Camera",
            min_time=1,
            max_time=5,
            min_amount=1,
        )
        self.url = reverse("dashboard-products-edit", args=[self.product.id])

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)


class ProductExtendedViewTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Test Product",
            quantity=10,
            category="Camera",
            min_time=1,
            max_time=5,
            min_amount=1,
        )
        self.product_extended = Product_extended.objects.create(
            name="Test Product Extended", SN="12345", status="available", faulty="NO"
        )
        self.url = reverse("dashboard-products-extended", args=[self.product.id])

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

class MyViewTests(TestCase):
    def test_request_new(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        product = Product.objects.create(name='Test Product')
        response = self.client.post(reverse('dashboard-index'), {
            'submit_button': 1,
            'product1': product.name,
            'time_value': ['7'],
        })
        self.assertEqual(Request.objects.count(), 1)
        self.assertEqual(response.status_code ,200)

    def test_request_approve(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        product = Product.objects.create(name='Test Product', min_amount=1)
        product_ex= Product_extended.objects.create(name="Test Product", SN="TestSN", status="Available")
        rented= Rented.objects.create(
            name="Test Product",
            username="Test User",
            SN="TestSN",
            status="Available",
            faulty="NO",
            start_time=timezone.datetime.now(),
            end_time=timezone.datetime.now(),
            explanation=0,
            question="Test",
            answer="Test"
        )
        request = Request.objects.create(name=product.name, username=user, date=timezone.now().date(), period=7)
        response = self.client.post(reverse('dashboard-request-approve', args=[product.name, user.username, 7]), {
            'submit_button': 1,
            f'product{request.id}': product_ex.SN,
        })
        self.assertEqual(Rented.objects.count(), 2)
        self.assertEqual(response.status_code ,302)
        
    def test_stock_request_deny(self):
        request_item = Stock_request.objects.create(
            name="Test Product",
            quantity=10,
        )
        response = self.client.post(reverse('deny', args=[request_item.name,"Test User",timezone.now().date(),7]))
        self.assertEqual(Stock_request.objects.count(), 1)
        self.assertEqual(response.status_code ,302)

    def test_reserve_staff(self):
        item = Product.objects.create(name='Test Product')
        product_ex=Product_extended.objects.create(name="Test Product Extended", SN="12345", status="Available", faulty="NO")
        response = self.client.post(reverse('dashboard-staff-reserve', args=[item.name]))
        self.assertEqual(Product_extended.objects.count(), 1)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(response.status_code ,200)

    def test_reserve_staff_students(self):
        item = Product.objects.create(name='Test Product')
        product_ex=Product_extended.objects.create(name="Test Product Extended", SN="12345", status="available", faulty="NO")
        response = self.client.post(reverse('dashboard-staff-reserve-students', args=[item.name]))
        self.assertEqual(Product_extended.objects.count(), 1)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(response.status_code ,200)

    def test_group_request(self):
        item = Product.objects.create(name='Test Product')
        user = User.objects.create_user(username='testuser', password='testpassword')
        self.assertEqual(Product.objects.count(), 1)


    def test_faults_show(self):
        response = self.client.post(reverse('dashboard-faults-show'))
        self.assertEqual(response.status_code ,200)

    
    