from django.contrib import admin
from .models import Expense

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('description', 'amount', 'category', 'date', 'created_by', 'created_at')
    list_filter = ('category', 'date')
    search_fields = ('description',)
