from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Product, Order, Product_extended, Rented, Request, Stock_request, MyList, Faults, Message
from .forms import (
    MyForm,
    ProductForm,
    OrderForm,
    dashboard_product_extended,
    RentedForm,
    RequestForm,
    Stock_RequestForm,
    fault_form,
    MessageForm,
)
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import auth_users, allowed_users
from django.http import QueryDict
from django.utils import timezone
from django.db.models import Q, Subquery, OuterRef, Count
from django.db import IntegrityError
from django.urls import reverse

def my_view(request):
    form = MyForm()
    return render(request, 'my_template.html', {'form': form})

@login_required(login_url="user-login")
def index(request):
    formlist = MyForm()
    productlist = MyList.objects.all()
    check = request.user.groups.filter(name="Staff").exists()
    product = Product.objects.all()
    product_count = product.count()
    rented = Rented.objects.all()
    rented_count = rented.count()
    customer = User.objects.filter(groups__in=[1, 2, 3])
    customer_count = customer.count()
    students = User.objects.filter(groups__in=[2])
    requests = Request.objects.all()
    requests_count = requests.count()
    curr_time = timezone.now().date()
    return_window_now = timezone.now().date() + timezone.timedelta(days=2)
    stock = Stock_request.objects.all()
    stock_count = stock.count()
    rented_group = Rented.objects.filter(username__contains= request.user.username)
    request_group = Request.objects.filter(username__contains= request.user.username)
    faults = Faults.objects.all()
    faults_count = faults.count()
    if request.method == "POST":
        if "faulty_button" in request.POST:
            faulty_order(request)
        elif "submit_button" in request.POST or "group_request" in request.POST:
            request_new(request)
        elif "return_button" in request.POST:
            return_order(request)
        elif "submit_staff_button" in request.POST:
            request_staff_new(request)
        elif "transfer_button" in request.POST:
            transfer_item(request)
        elif "list_button" in request.POST:
            new_list(request)
        form = RentedForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.customer = request.user
            obj.save()
            return redirect("dashboard-index")
    else:
        form = RentedForm()
    context = {  # All the items that I'd like to send to the HTML
        "form": form,
        "rented": rented,
        "product": product,
        "product_count": product_count,
        "rented_count": rented_count,
        "customer_count": customer_count,
        "username_": request.user.username,
        "request_count": requests_count,
        "stock_count": stock_count,
        "requests": requests,
        "user_in_group": check,
        "curr_time": curr_time,
        "return_window_now": return_window_now,
        "students": students,
        "rented_group":rented_group,
        "request_group": request_group,
        "formlist": formlist,
        "productlist":productlist,
        "faults_count": faults_count,
    }
    return render(request, "dashboard/index.html", context)

@login_required(login_url="user-login")
def products(request):
    product = Product.objects.all()
    #productex = Product_extended.objects.all()
    product_count = product.count()
    customer = User.objects.filter(groups__in=[1, 2, 3])
    customer_count = customer.count()
    rented = Rented.objects.all()
    rented_count = rented.count()
    requests = Request.objects.all()
    requests_count = requests.count()
    #product_quantity = Product.objects.filter(name="")
    stock = Stock_request.objects.all()
    stock_count = stock.count()
    faults = Faults.objects.all()
    faults_count = faults.count()
    studentlist = User.objects.filter(groups__in=[2])
    stafflist = User.objects.filter(groups__in=[3])
    if request.method == "POST":
        post_data = QueryDict(request.POST.urlencode(), mutable=True)
        post_data["SN"] = "NULL"
        post_data["status"] = "Available"
        post_data["faulty"] = "NO"
        form = ProductForm(request.POST, request.FILES)
        quantity = int(request.POST["quantity"])    
        request.POST = post_data
        if form.is_valid():
            form.save()
            for _ in range(quantity):
                form2 = dashboard_product_extended(request.POST)
                if form2.is_valid():
                    form2.save()
            product_name = form.cleaned_data.get("name")
            messages.success(request, f"{product_name} has been added")
            return redirect("dashboard-products")
        else:
            print("form invalid")
            print(form.errors)
    else:
        form = ProductForm()
    context = {
        "product": product,
        "form": form,
        "customer_count": customer_count,
        "product_count": product_count,
        "rented_count": rented_count,
        "request_count": requests_count,
        "stock_count": stock_count,
        "faults_count": faults_count,
        "studentlist" : studentlist,
        "stafflist" : stafflist,
    }
    return render(request, "dashboard/products.html", context)

@login_required(login_url="user-login")
def product_detail(request, pk):
    context = {}
    return render(request, "dashboard/products_detail.html", context)

@login_required(login_url="user-login")
def customers(request):
    customer = User.objects.filter(groups__in=[1, 2, 3])
    customer_count = customer.count()
    product = Product.objects.all()
    product_count = product.count()
    rented = Rented.objects.all()
    rented_count = rented.count()
    requests = Request.objects.all()
    requests_count = requests.count()
    stock = Stock_request.objects.all()
    stock_count = stock.count()
    faults = Faults.objects.all()
    faults_count = faults.count()
    context = {
        "customer": customer,
        "customer_count": customer_count,
        "product_count": product_count,
        "rented_count": rented_count,
        "request_count": requests_count,
        "stock_count": stock_count,
        "faults_count": faults_count,
    }
    return render(request, "dashboard/customers.html", context)

@login_required(login_url="user-login")
def requests(request):
    customer = User.objects.filter(groups__in=[1, 2, 3])
    customer_count = customer.count()
    product = Product.objects.all()
    product_count = product.count()
    rented = Rented.objects.all()
    rented_count = rented.count()
    requests = Request.objects.all()
    requests_count = requests.count()
    stock = Stock_request.objects.all()
    stock_count = stock.count()
    faults = Faults.objects.all()
    faults_count = faults.count()
    studentlist = User.objects.filter(groups__in=[2])
    stafflist = User.objects.filter(groups__in=[3])

    context = {
        "customer": customer,
        "customer_count": customer_count,
        "product_count": product_count,
        "rented_count": rented_count,
        "request_count": requests_count,
        "requests": requests,
        "stock_count": stock_count,
        "faults_count": faults_count,
        "studentlist" : studentlist,
        "stafflist" : stafflist,
    }

    return render(request, "dashboard/customer_requests.html", context)

@login_required(login_url="user-login")
@allowed_users(allowed_roles=["Admin"])
def customer_detail(request, pk):
    customer = User.objects.filter(groups__in=[1, 2, 3])
    customer_count = customer.count()
    product = Product.objects.all()
    product_count = product.count()
    rented = Rented.objects.all()
    rented_count = rented.count()
    requests = Request.objects.all()
    requests_count = requests.count()
    customers = User.objects.get(id=pk)
    stock = Stock_request.objects.all()
    stock_count = stock.count()
    faults = Faults.objects.all()
    faults_count = faults.count()

    context = {
        "customers": customers,
        "customer_count": customer_count,
        "product_count": product_count,
        "rented_count": rented_count,
        "request_count": requests_count,
        "stock_count": stock_count,
        "faults_count": faults_count,
    }
    return render(request, "dashboard/customers_detail.html", context)

@login_required(login_url="user-login")
@allowed_users(allowed_roles=["Admin"])
def product_edit(request, pk):
    item = Product.objects.get(id=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect("dashboard-products")
    else:
        form = ProductForm(instance=item)
    context = {
        "form": form,
    }
    return render(request, "dashboard/products_edit.html", context)

@login_required(login_url="user-login")
def request_approve(request, product, user, period):
    item = Product.objects.get(name=product)
    products = Product_extended.objects.filter(
        Q(name=product), Q(status="Available") | Q(status__startswith="Reserved:")
    )
    requested_item = Request.objects.get(name=product, username=user, period=period)
    if request.method == "POST":
        if "submit_button" in request.POST:
            button_index = int(request.POST["submit_button"])
            product_sn = request.POST[f"product{button_index}"]
            name = product
            username = user
            SN = product_sn
            status = f"Rented: {username}"
            faulty = "NO"
            start_time = timezone.now().date()
            end_time = timezone.now().date() + timezone.timedelta(days=period)

            form_data = {
                "name": name,
                "username": username,
                "SN": SN,
                "status": status,
                "faulty": faulty,
                "start_time": start_time,
                "end_time": end_time,
                "explanation": 0,
                "question": 0,
                "answer": 0,
            }
            form = RentedForm(data=form_data)
            if form.is_valid():
                form.save()
                requested_item.delete()
                min_amount = item.min_amount
                item.available = (
                    Product_extended.objects.filter(
                        name=name, status="Available"
                    ).count()
                    - min_amount
                )
                item.save()
                product_ex = Product_extended.objects.get(name=name, SN=SN)
                product_ex.status = f"Rented: {username}"
                product_ex.save()
                return redirect("dashboard-index")
            else:
                print("Form data is invalid")
                print(form_data)
                print(form.errors)

    context = {
        "item": item,
        "requested_item": requested_item,
        "products": products,
    }
    return render(request, "dashboard/request_approve.html", context)

def request_deny(request, product, user, date, period):
    request_item = Request.objects.filter(
        name=product, username=user, date=date, period=period
    )
    request_item.delete()
    return redirect("dashboard-requests")

def request_new(request):
    if request.method == "POST":
        if "submit_button" in request.POST:
            button_index = int(request.POST["submit_button"])
            product_name = request.POST[f"product{button_index}"]
            time = timezone.now().date()
            time_value = request.POST.getlist("time_value")
            period = time_value[button_index - 1]
            username = request.user
            form_data = {
                "name": product_name,
                "username": username,
                "date": time,
                "period": period,
            }
            form = RequestForm(data=form_data)
            if form.is_valid():
                form.save()
            else:
                print("Form data is invalid")
                print(form_data)
                print(form.errors)
        # elif "group_request" in request.POST:
        #     print("here")
        #     button_index = int(request.POST["group_request"])
        #     product_name = request.POST[f"group{button_index}"]
        #     time = timezone.now().date()
        #     time_value = request.POST.getlist("time_value")
        #     period = time_value[button_index - 1]
        #     return render(request, "dashboard/group_request.html")

    context = {
        "products": products,
    }
    return render(request, "dashboard/index.html", context)

def request_staff_new(request):
    if request.method == "POST":
        button_index = int(request.POST["submit_staff_button"])
        product_name = request.POST[f"product{button_index}"]
        time = timezone.now().date()
        username = request.user
        form_data = {
            "name": product_name,
            "username": username,
            "date": time,
            "period": 0,
        }
        form = RequestForm(data=form_data)
        if form.is_valid():
            print(form_data)
            form.save()
        else:
            print("Form data is invalid")
            print(form_data)
            print(form.errors)

    context = {
        "products": products,
    }
    return render(request, "dashboard/index.html", context)

def reserve_staff(request, product):
    item = Product.objects.get(name=product)
    products = Product_extended.objects.filter(
        Q(status="Available") | Q(status=f"Reserved: {request.user}")
    ).filter(name=product)
    if request.method == "POST":
        if "submit_button" in request.POST:
            button_index = int(request.POST["submit_button"])
            product_sn = request.POST[f"product{button_index}"]
            name = product
            SN = product_sn
            product_ex = Product_extended.objects.get(name=name, SN=SN)
            product_ex.status = f"Reserved: {request.user}"
            product_ex.save()
            return redirect("dashboard-index")

    context = {
        "item": item,
        "products": products,
    }
    return render(request, "dashboard/staff_reserve.html", context)

def reserve_staff_students(request, product):
    item = Product.objects.get(name=product)
    products = Product_extended.objects.filter(name=product, status="Available")
    if request.method == "POST":
        if "under_button" in request.POST:
            amount_needed_str = request.POST["amount_needed"]
            if amount_needed_str is not None:
                amount_needed = int(amount_needed_str)
                product_ex = Product_extended.objects.filter(
                    name=product, status="Available"
                )[:amount_needed].values_list("id", flat=True)
                Product_extended.objects.filter(id__in=product_ex).update(
                    status="Reserved"
                )

            else:
                print("Amount needed None")
            return redirect("dashboard-index")

    context = {
        "item": item,
        "products": products,
    }
    return render(request, "dashboard/staff_reserve_students.html", context)

def return_order(request):
    if request.method == "POST":
        button_index = int(request.POST["return_button"])
        product_str = request.POST[f"product{button_index}"]
        product_name, product_SN = product_str.split(";")

        product_ex = Product_extended.objects.get(name=product_name, SN=product_SN)
        product_ex.status = "Available"
        product_ex.save()
        item = Product.objects.get(name=product_name)
        min_amount = item.min_amount
        item.available = (
            Product_extended.objects.filter(
                name=product_name, status="Available"
            ).count()
            - min_amount
        )
        item.save()
        rented_item = Rented.objects.get(
            name=product_name,
            SN=product_SN,
        )
        rented_item.delete()
    context = {
        "products": products,
    }
    return render(request, "dashboard/index.html", context)

def faulty_order(request):
    if request.method == "POST":
        button_index = int(request.POST["faulty_button"])
        product_str = request.POST[f"product{button_index}"]
        product_name, product_SN = product_str.split(";")

        product_ex = Product_extended.objects.get(name=product_name, SN=product_SN)
        product_ex.status = "Faulty"
        product_ex.faulty = "YES"
        product_ex.save()
        item = Product.objects.get(name=product_name)
        min_amount = item.min_amount
        item.available = (
            Product_extended.objects.filter(
                name=product_name, status="Available"
            ).count()
            - min_amount
        )
        item.save()
        rented_item = Rented.objects.get(
            name=product_name,
            SN=product_SN,
        )
        rented_item.delete()
    context = {
        "products": products,
    }
    return render(request, "dashboard/index.html", context)

def student_explain(request):
    if request.method == "POST":
        button_index = int(request.POST["explain_button"])
        product_str = request.POST[f"product{button_index}"]
        product_name, product_SN = product_str.split(";")
        rented_item = Rented.objects.get(
            name=product_name,
            SN=product_SN,
        )
        rented_item.explanation = 1
        rented_item.save()
    context = {
        "products": products,
    }
    return render(request, "dashboard/index.html", context)

@login_required(login_url="user-login")
@allowed_users(allowed_roles=["Admin"])
def product_edit_extended(request, pk):
    item = Product_extended.objects.get(id=pk)
    if request.method == "POST":
        form = dashboard_product_extended(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect("dashboard-products")
    else:
        form = dashboard_product_extended(instance=item)
    context = {
        "form": form,
    }
    return render(request, "dashboard/products_extended_edit.html", context)

@login_required(login_url="user-login")
def product_delete(request, pk):
    item = Product.objects.get(id=pk)
    if request.method == "POST":
        Product_extended.objects.filter(name=item.name).delete()
        item.delete()
        return redirect("dashboard-products")
    context = {"item": item}
    return render(request, "dashboard/products_delete.html", context)

@login_required(login_url="user-login")
def order(request):
    rented = Rented.objects.all()
    rented_count = rented.count()
    customer = User.objects.filter(groups__in=[1, 2, 3])
    customer_count = customer.count()
    product = Product.objects.all()
    product_count = product.count()
    requests = Request.objects.all()
    requests_count = requests.count()
    curr_time = timezone.now().date()
    stock = Stock_request.objects.all()
    stock_count = stock.count()
    faults = Faults.objects.all()
    faults_count = faults.count()
    studentlist = User.objects.filter(groups__in=[2])
    stafflist = User.objects.filter(groups__in=[3])
    context = {
        "rented": rented,
        "customer_count": customer_count,
        "product_count": product_count,
        "rented_count": rented_count,
        "request_count": requests_count,
        "curr_time": curr_time,
        "stock_count": stock_count,
        "faults_count": faults_count,
        "studentlist": studentlist,
        "stafflist" : stafflist
    }
    return render(request, "dashboard/rented.html", context)

@login_required(login_url="user-login")
def product_extended(request, pk):
    product = Product_extended.objects.filter(name=pk)
    if request.method == "POST":
        form2 = dashboard_product_extended(request.POST)
        if form2.is_valid():
            form2.save()
            return redirect("dashboard-products")
    else:
        form = ProductForm()
    context = {
        "form": form,
        "product": product,
    }
    return render(request, "dashboard/products_extended.html", context)

def transfer_item(request):
    button_index = int(request.POST["transfer_button"])
    product_str = request.POST[f"product{button_index}"]
    product_name, product_SN = product_str.split(";")
    new_user = request.POST["transfer_list"]

    rented_item = Rented.objects.get(
        name=product_name,
        SN=product_SN,
    )
    rented_item.username = new_user
    rented_item.status = f"Rented: {new_user}"
    rented_item.save()

    product_ex = Product_extended.objects.get(name=product_name, SN=product_SN)
    product_ex.status = f"Rented: {new_user}"
    product_ex.save()

    return 0

def question_answer(request, rented, rentedSN):
    check = request.user.groups.filter(name="Staff").exists()
    rented_item = Rented.objects.get(
        name=rented,
        SN=rentedSN,
    )
    if request.method == "POST":
        if "send_question_button" in request.POST:
            rented_item.explanation = 1
            question = request.POST.get("question")
            rented_item.question = question
            rented_item.save()
        if "send_answer_button" in request.POST:
            rented_item.explanation = 1
            answer = request.POST.get("answer")
            rented_item.answer = answer
            rented_item.save()
    context = {
        "rented_item": rented_item,
        "user_in_group": check,
    }
    return render(request, "dashboard/question_answer.html", context)

def request_more(request, name):
    item = Product.objects.get(name=name)
    if request.method == "POST":
        amount_needed_str = request.POST["amount_needed"]
        if amount_needed_str is not None:
            amount_needed = int(amount_needed_str)
            form_data = {
                "name": name,
                "quantity": amount_needed,
            }
            form = Stock_RequestForm(data=form_data)
            if form.is_valid():
                form.save()
                return redirect("dashboard-index")
            else:
                print("Form data is invalid")
                print(form_data)
                print(form.errors)
        else:
            print("amount needed none")
    context = {"item": item}
    return render(request, "dashboard/stock_requests.html", context)

def stock_requests_show(request):
    customer = User.objects.filter(groups__in=[1, 2, 3])
    customer_count = customer.count()
    product = Product.objects.all()
    product_count = product.count()
    rented = Rented.objects.all()
    rented_count = rented.count()
    requests = Request.objects.all()
    requests_count = requests.count()
    stock = Stock_request.objects.all()
    stock_count = stock.count()
    faults = Faults.objects.all()
    faults_count = faults.count()

    context = {
        "customer": customer,
        "customer_count": customer_count,
        "product_count": product_count,
        "rented_count": rented_count,
        "request_count": requests_count,
        "requests": requests,
        "stock_count": stock_count,
        "stock": stock,
        "faults_count": faults_count,
    }

    return render(request, "dashboard/stock_requests_show.html", context)

def stock_request_deny(request, product, quantity):
    request_item = Stock_request.objects.filter(name=product, quantity=quantity)
    request_item.delete()
    return redirect("stock-requests-show")

def group_request(request, name, time):
    students = User.objects.filter(groups__in=[2])
    product = Product.objects.get(name=name)
    current_time = timezone.now().date()
    time_value = request.POST.get('time_value')
    if request.method == "POST":
        selected_users = request.POST.getlist("selected_users")
        username = str(request.user) + ", " + ", ".join(str(user) for user in selected_users)
        # username = ", ".join(selected_users)
        form_data = {
            "name": name,
            "username": username,
            "date": current_time,
            "period": time_value,
        }
        form = RequestForm(data=form_data)
        if form.is_valid():
            form.save()
        else:
            print("Form data is invalid")
            print(form_data)
            print(form.errors)
    context = {
        "product_name": name,
        "students": students,
        "username_": request.user.username,
        "product": product,
    }

    return render(request, "dashboard/group_request.html", context)

def new_list(request):
    prodList="Equipment:"
    if 'Sony A7III' in request.POST:
        prodList+=" Sony A7III"
    if 'Panasonic DC-S5' in request.POST:
        prodList+=" Panasonic DC-S5"
    if 'Rode micro mic' in request.POST:
        prodList+=" Rode micro mic"
    if 'iPad Pro' in request.POST:
        prodList+=" iPad Pro"
    if 'Manfrotto 190X' in request.POST:
        prodList+=" Manfrotto 190X"
    if 'Manfrotto BeFree Advanced' in request.POST:
        prodList+=" Manfrotto BeFree Advanced"
    form_data = {
        "className" : request.POST.get('class_name'),
        "productList": prodList,
    }
    form = MyForm(data=form_data)
    if form.is_valid():
        form.save()
    else:
        print("Form data is invalid .")
        print(form_data)
        print(form.errors)
    return 0

def faults_report(request, pk, name):
    formParameters = {
        "product_name": name,
        "SN": pk,
        "report_time": timezone.now().date(),
        "category": "NO",
        "fault_description": "",
    }

    form_faulty = fault_form(data=formParameters)
    if form_faulty.is_valid():
        if not Faults.objects.filter(product_name=form_faulty.cleaned_data['product_name'], SN=form_faulty.cleaned_data['SN']).exists():
            try:
                form_faulty.save()
            except IntegrityError:
                pass
    else:
        print("Form data is invalid")
        print(formParameters)
        print(form_faulty.errors)
    item_faults = Faults.objects.get(product_name=name, SN=pk)
    if request.method == "POST":
        product_ex = Product_extended.objects.get(name= name, SN=pk)
        product_ex.status = "Faulty"
        product_ex.faulty = "YES"
        product_ex.save()
        item = Product.objects.get(name=name)
        min_amount = item.min_amount
        if Product_extended.objects.filter(
                name=name, status="Available"
            ).count() >0:
            item.available = (Product_extended.objects.filter(name=name, status="Available").count()- min_amount
        )
        item.save()
        rented_item = Rented.objects.get(
            name=name,
            SN=pk,
        )
        rented_item.delete()
        item_faults.category=request.POST.get('category')
        item_faults.fault_description=request.POST.get('fault_description')
        item_faults.save()
        return redirect("dashboard-index")
    else:
        form_faulty = fault_form(instance=item_faults)
    context = {
       "form": form_faulty,
        }
    return render(request, "dashboard/faults.html", context)

def faults_show(request):
    customer = User.objects.filter(groups__in=[1, 2, 3])
    customer_count = customer.count()
    product = Product.objects.all()
    product_count = product.count()
    rented = Rented.objects.all()
    rented_count = rented.count()
    requests = Request.objects.all()
    requests_count = requests.count()
    stock = Stock_request.objects.all()
    stock_count = stock.count()
    faults = Faults.objects.all()
    faults_count = faults.count()
    context = {
        "customer": customer,
        "faults": faults,
        "customer_count": customer_count,
        "product_count": product_count,
        "rented_count": rented_count,
        "request_count": requests_count,
        "stock_count": stock_count,
        "faults_count": faults_count,
    }
    return render(request, "dashboard/faults_display.html", context)

def get_messages(request):
    messages = Message.objects.filter(reciever=request.user).order_by('time')
    senders = Message.objects.filter(reciever=request.user).values('sender').distinct()
    sendersunread = Message.objects.filter(
        reciever=request.user,
        undreadrec=1
    ).values('sender').annotate(message_count=Count('sender')).filter(message_count__gt=0)

    users = User.objects.exclude(username=request.user.username).exclude(username__in=senders)
    context = {
        "messages" : messages,
        "senders" : senders,
        "new_chat": 0,
        "users": users,
        "sendersunread" : sendersunread,
    }
    if request.method == "POST":
        if "submit_button" in request.POST:
            button_index = int(request.POST["submit_button"])
            sender = request.POST[f"product{button_index}"]
            return redirect(reverse('dashboard-chat-open', args=[sender]))
        elif "new_chat_button" in request.POST:
            button_index = int(request.POST["new_chat_button"])
            sender = request.POST[f"chat{button_index}"]
            return redirect(reverse('dashboard-chat-open', args=[sender]))

        else:
            context["new_chat"] = 1
               
    return render(request, "dashboard/chat.html", context)

def read_messages(request , sender):
    messages = Message.objects.filter(
    Q(reciever=request.user, sender=sender) | Q(reciever=sender, sender=request.user)
        ).order_by('time')
    read_messages = Message.objects.filter(reciever=request.user, sender=sender)
    read_messages.update(undreadrec=0)
    if request.method == "POST":
        message = request.POST.get('message')
        form_data = {
        "sender" : request.user,
        "reciever": sender,
        "content": message,
        "time": timezone.now(),  
        "undreadrec" : 1,
        "unreadsend" : 0,      
        }
        form=MessageForm(form_data)
        if form.is_valid():
            form.save()
        else:
            print("form invalid")
            print(form.errors)
    context = {
        "messages" : messages,
        "sender": sender,
    }
    return render(request, "dashboard/chat_open.html", context)