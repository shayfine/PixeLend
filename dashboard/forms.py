from django import forms
from .models import Product, Order, Product_extended, Request, Rented, Stock_request, MyList, Faults, Message

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"

class MyForm(forms.ModelForm):
    class Meta:
        model = MyList
        fields = ["className", "productList"]

class dashboard_product_extended(forms.ModelForm):
    class Meta:
        model = Product_extended
        fields = ["name", "SN", "status", "faulty"]

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["name", "order_quantity"]

class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ["name", "username", "date", "period"]

class RentedForm(forms.ModelForm):
    class Meta:
        model = Rented
        fields = ["name", "username", "SN", "status", "faulty", "start_time", "end_time", "explanation", "question", "answer"]

class Stock_RequestForm(forms.ModelForm):
    class Meta:
        model = Stock_request
        fields = ["name", "quantity"]

class fault_form(forms.ModelForm):
    class Meta:
        model = Faults
        fields = ["product_name", "SN", "report_time", "category", "fault_description"]
        
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["sender", "reciever", "content", "time", "undreadrec", "unreadsend"]
        