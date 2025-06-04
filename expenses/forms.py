from django import forms
from .models import Expense

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['property', 'description', 'amount', 'category', 'date']  # Add 'property'
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }