from django.contrib import admin
from .models import Visitor

@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    list_display = ('name', 'whom_to_visit', 'purpose', 'check_in', 'check_out')
    search_fields = ('name', 'whom_to_visit__username', 'purpose')
    list_filter = ('check_in', 'check_out')
