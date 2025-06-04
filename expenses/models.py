from django.db import models
from django.contrib.auth import get_user_model
from properties.models import Building  # Adjust if your model is named differently

class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('maintenance', 'Maintenance'),
        ('utilities', 'Utilities'),
        ('staff', 'Staff'),
        ('supplies', 'Supplies'),
        ('other', 'Other'),
    ]
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    date = models.DateField()
    property = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='expenses', null=True, blank=True)  # <-- Add this line
    created_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.description} ({self.amount})"
