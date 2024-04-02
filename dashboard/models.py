from datetime import timezone
from django import forms
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
CATEGORY = (
    ("Camera", "Camera"),
    ("Recording", "Recording"),
    ("Tablet", "Tablet"),
    ("Tripod", "Tripod"),
)


# FAULTS = (
#     ('Technical Fault', 'Technical Fault'), ('Mechanical Fault','Mechanical Fault' ), ('Other', "Other")
# )

FAULTY = (
    ("Available", "Available"),
    ("Technical Fault", "Technical Fault"),
    ("Mechanical Fault", "Mechanical Fault"),
    ("Other", "Other"),
    ("NO", "NO"),
)


MY_CHOICES = (
        ('Sony A7III', 'Sony A7III'),
        ('Panasonic DC-S5', 'Panasonic DC-S5'),
        ('Rode micro mic', 'Rode micro mic'),
        ('iPad Pro', 'iPad Pro'),
        ('Manfrotto 190X', 'Manfrotto 190X'),
        ('Manfrotto BeFree Advanced', 'Manfrotto BeFree Advanced'),
    )


class MyList(models.Model):
    className = models.CharField(max_length=100,null=True)
    productList = models.CharField(max_length=100,null=True)

    def __str__(self):
        return f'{self.name}'
    def strip(value):
        return value.strip()


class Product(models.Model):
    name = models.CharField(max_length=100, null=True)
    quantity = models.PositiveIntegerField(null=True)
    category = models.CharField(max_length=50, choices=CATEGORY, null=True)
    min_time = models.PositiveIntegerField(null=True)
    max_time = models.PositiveIntegerField(null=True)
    min_amount = models.PositiveIntegerField(null=True)
    available = models.PositiveBigIntegerField(null=True)
    photo = models.ImageField(upload_to = 'media/', null=True, blank=True)

    def __str__(self):
        return f"{self.name}"

    def strip(value):
        return value.strip()


class Product_extended(models.Model):
    name = models.CharField(max_length=100, null=True)
    SN = models.CharField(max_length=50, null=True)
    status = models.CharField(max_length=50, null=True)
    faulty = models.CharField(max_length=50, choices=FAULTY, null=True)

    def __str__(self):
        return f"{self.name}"

    def strip(value):
        return value.strip()


class Order(models.Model):
    name = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    order_quantity = models.PositiveIntegerField(null=True)

    def __str__(self):
        return f"{self.name}"


class Request(models.Model):
    name = models.CharField(max_length=100, null=True)
    username = models.CharField(max_length=100, null=True)
    date = models.DateField()
    period = models.PositiveIntegerField(null=True)

    def __str__(self):
        return f"{self.name}"

    def strip(value):
        return value.strip()


class Rented(models.Model):
    name = models.CharField(max_length=100, null=True)
    username = models.CharField(max_length=100, null=True)
    SN = models.CharField(max_length=50, null=True)
    status = models.CharField(max_length=50, null=True)
    faulty = models.CharField(max_length=50, choices=FAULTY, null=True)
    start_time = models.DateField()
    end_time = models.DateField()
    explanation = models.PositiveIntegerField(null=True)
    question = models.CharField(max_length=1000, null=True)
    answer = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return f"{self.name}"

    def strip(value):
        return value.strip()


class Stock_request(models.Model):
    name = models.CharField(max_length=100, null=True)
    quantity = models.PositiveIntegerField(null=True)

    def __str__(self):
        return f"{self.name}"

    def strip(value):
        return value.strip()


class Faults(models.Model):
    product_name = models.CharField(max_length=100, null=True)
    SN = models.CharField(max_length=50, null=True)
    report_time = models.DateField()
    category = models.CharField(max_length=50, choices=FAULTY, null=True)
    fault_description = models.CharField(max_length=500, blank=True, default=None)

    def __str__(self):
        return f"{self.name}"

    def strip(value):
        return value.strip()

class Message(models.Model):
    sender = models.CharField(max_length=100, null=True)
    reciever = models.CharField(max_length=100, null=True)
    content = models.CharField(max_length=500, null=True)
    time = models.DateTimeField()
    undreadrec = models.PositiveIntegerField(null=True)
    unreadsend = models.PositiveIntegerField(null=True)

    def __str__(self):
        return f"{self.name}"

    def strip(value):
        return value.strip()