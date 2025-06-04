from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Expense
from .forms import ExpenseForm

@login_required
def expense_list(request):
    user = request.user
    if user.is_superuser:
        expenses = Expense.objects.all().order_by('-date')
    elif hasattr(user, "role"):
        if user.role == "landlord":
            # Landlord sees all expenses for their properties and all expenses created by employees (agents, caretakers)
            expenses = Expense.objects.filter(
                property__landlord=user
            ).order_by('-date')
        elif user.role in ["agent", "caretaker"]:
            # Employees see all expenses for properties they manage or create
            expenses = Expense.objects.filter(
                property__agent=user
            ).order_by('-date') | Expense.objects.filter(
                property__caretaker=user
            ).order_by('-date') | Expense.objects.filter(
                created_by=user
            ).order_by('-date')
            expenses = expenses.distinct().order_by('-date')
        else:
            expenses = Expense.objects.filter(created_by=user).order_by('-date')
    else:
        expenses = Expense.objects.none()
    return render(request, "expenses/expense_list.html", {"expenses": expenses})

@login_required
def expense_create(request):
    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.created_by = request.user
            expense.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm()
    return render(request, "expenses/expense_create.html", {"form": form})

@login_required
def expense_detail(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    return render(request, "expenses/expense_detail.html", {"expense": expense})
