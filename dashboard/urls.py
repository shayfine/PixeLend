from django.urls import include, path
from . import views

urlpatterns = [
    path('', include('django_prometheus.urls')),
    path("index/", views.index, name="dashboard-index"),
    path("products/", views.products, name="dashboard-products"),
    path(
        "products/delete/<int:pk>/",
        views.product_delete,
        name="dashboard-products-delete",
    ),
    path(
        "products/detail/<int:pk>/",
        views.product_detail,
        name="dashboard-products-detail",
    ),
    path("products/edit/<int:pk>/", views.product_edit, name="dashboard-products-edit"),
    path(
        "products/extended/extended/edit/<int:pk>/",
        views.product_edit_extended,
        name="dashboard-products-extended-edit",
    ),
    path("customers/", views.customers, name="dashboard-customers"),
    path(
        "customers/detial/<int:pk>/",
        views.customer_detail,
        name="dashboard-customer-detail",
    ),
    path("order/", views.order, name="dashboard-order"),
    path(
        "products/extended/<str:pk>/",
        views.product_extended,
        name="dashboard-products-extended",
    ),
    path("requests", views.requests, name="dashboard-requests"),
    path("requests_show", views.stock_requests_show, name="stock-requests-show"),
    path(
        "request/deny/<str:product>/<int:quantity>",
        views.stock_request_deny,
        name="deny-stock-request",
    ),
    path(
        "request/approve/<str:product>/<str:user>/<int:period>",
        views.request_approve,
        name="dashboard-request-approve",
    ),
    path(
        "request/deny/<str:product>/<str:user>/<str:date>/<int:period>",
        views.request_deny,
        name="deny",
    ),
    path(
        "staff/reserve/<str:product>",
        views.reserve_staff,
        name="dashboard-staff-reserve",
    ),
    path(
        "staff/reserve/students/<str:product>",
        views.reserve_staff_students,
        name="dashboard-staff-reserve-students",
    ),
    path(
        "question_answer/<str:rented>/<str:rentedSN>",
        views.question_answer,
        name="dashboard-question-answer",
    ),
    path("request/more/<str:name>", views.request_more, name="request-more"),
    path(
        "dashboard/group_request/<str:name>/<int:time>",
        views.group_request,
        name="group-request",
    ),
    path(
        "dashboard/faults/<str:pk>/<str:name>",
        views.faults_report,
        name="Faults",
    ),
    path(
        "dashboard/faults_display",
        views.faults_show,
        name="dashboard-faults-show",
    ),
    path(
        "dashboard/chat",
        views.get_messages,
        name="dashboard-chat"
    ),
    path(
        "dashboard/chat_open/<str:sender>",
        views.read_messages,
        name="dashboard-chat-open"
    )
]
