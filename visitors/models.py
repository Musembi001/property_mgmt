from django.db import models
from django.contrib.auth import get_user_model
from properties.models import Building  # If you want to link to a property

class Visitor(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    whom_to_visit = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True, related_name='visitors')
    purpose = models.CharField(max_length=255)
    check_in = models.DateTimeField(auto_now_add=True)
    check_out = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    registered_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True, related_name='registered_visitors')
    property = models.ForeignKey(Building, on_delete=models.SET_NULL, null=True, blank=True, related_name='visitors')  # Optional

    def __str__(self):
        return f"{self.name} visiting {self.whom_to_visit}"
