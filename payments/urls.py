from django.urls import path
from . import views

urlpatterns = [
    path("", views.payment_options, name="payment_options"),
    path("mpesa/", views.mpesa_payment, name="mpesa_payment"),
    path("mpesa/callback/", views.mpesa_callback, name="mpesa_callback"),
    path("other/", views.other_payment, name="other_payment"),
    path("receipt/<int:payment_id>/", views.payment_receipt, name="payment_receipt"),
    path("receipt/<int:payment_id>/download/", views.download_receipt_pdf, name="download_receipt_pdf"),
    path("add/", views.add_payment, name="add_payment"),
]