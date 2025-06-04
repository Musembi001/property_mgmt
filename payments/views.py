from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from .models import Payment
from .forms import PaymentForm
from .mpesa import lipa_na_mpesa_online
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import io
from xhtml2pdf import pisa

@login_required
def payment_options(request):
    return render(request, "payments/payment_options.html")

@login_required
def mpesa_payment(request):
    if request.method == "POST":
        phone = request.POST.get("phone")
        amount = request.POST.get("amount")
        # You may want to link to a lease or invoice here
        response = lipa_na_mpesa_online(phone, amount, "Rent", "Rent Payment")
        if response.get("ResponseCode") == "0":
            messages.success(request, "M-PESA prompt sent. Complete payment on your phone.")
        else:
            messages.error(request, f"Payment failed: {response.get('errorMessage', 'Unknown error')}")
    return render(request, "payments/mpesa_payment.html")

@csrf_exempt
def mpesa_callback(request):
    # Handle M-PESA callback here (update Payment record)
    # Example: parse JSON, find Payment by reference, mark as paid
    return HttpResponse("OK")

@login_required
def other_payment(request):
    method = request.GET.get("method", "manual")
    method_names = {
        "airtel": "Airtel Money",
        "tkash": "T-Kash",
        "bank": "Bank Transfer",
        "manual": "Manual Payment",
    }
    instructions = {
        "airtel": "Send payment to our Airtel Money number: <strong>0733 123456</strong>.<br>Enter the transaction reference and upload your confirmation screenshot.",
        "tkash": "Pay via T-Kash to our T-Kash number: <strong>123456</strong>.<br>Enter the transaction reference and upload your confirmation screenshot.",
        "bank": "Transfer to our bank account:<br><strong>Account Name:</strong> Property Management Ltd<br><strong>Account Number:</strong> 011234567890<br><strong>Bank:</strong> KCB<br>Upload your deposit slip and enter the reference.",
        "manual": "Pay cash at our office. Upload your receipt or get it verified by our staff.",
    }
    if request.method == "POST":
        form = PaymentForm(request.POST, request.FILES)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.method = method
            payment.status = "pending"
            payment.save()
            messages.success(request, "Payment submitted. Awaiting verification.")
            return redirect("payment_receipt", payment_id=payment.id)
    else:
        form = PaymentForm()
    return render(request, "payments/other_payment.html", {
        "form": form,
        "method": method,
        "method_name": method_names.get(method, "Manual Payment"),
        "instructions": instructions.get(method, ""),
    })

@login_required
def payment_receipt(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    return render(request, "payments/receipt.html", {"payment": payment})

@login_required
def download_receipt_pdf(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    html = render_to_string("payments/receipt.html", {"payment": payment})
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="receipt_{payment.id}.pdf"'
    pisa.CreatePDF(io.BytesIO(html.encode("UTF-8")), dest=response)
    return response

@login_required
def add_payment(request):
    if request.method == "POST":
        form = PaymentForm(request.POST, request.FILES)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.status = "pending"
            payment.save()
            messages.success(request, "Payment recorded successfully and is pending verification.")
            return redirect("payment_receipt", payment_id=payment.id)
    else:
        form = PaymentForm()
    return render(request, "payments/add_payment.html", {"form": form})

@login_required
def payment_list(request):
    user = request.user
    if hasattr(user, "role"):
        if user.role == "tenant":
            # Show only payments made by this tenant
            payments = Payment.objects.filter(user=user)
        elif user.role == "landlord":
            # Show payments for properties owned by landlord (adjust field as needed)
            payments = Payment.objects.filter(lease__unit__property__landlord=user)
        elif user.role == "agent":
            # Show payments for properties managed by agent (adjust field as needed)
            payments = Payment.objects.filter(lease__unit__property__agent=user)
        elif user.role == "caretaker":
            # Show payments for properties managed by caretaker (adjust field as needed)
            payments = Payment.objects.filter(lease__unit__property__caretaker=user)
        else:
            payments = Payment.objects.none()
    else:
        payments = Payment.objects.none()
    return render(request, "payments/payment_list.html", {"payments": payments})
