from django.db import models
from django.contrib.auth import get_user_model
from properties.models import Building  # Make sure this import matches your property model

class AuditLog(models.Model):
    ACTION_CHOICES = [
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('login', 'Login'),
        ('logout', 'Logout'),
        # Add more as needed
    ]
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    model_name = models.CharField(max_length=100)
    object_id = models.CharField(max_length=100)
    object_repr = models.CharField(max_length=255)
    changes = models.TextField(blank=True, null=True)  # JSON or text describing the change
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    property = models.ForeignKey(Building, null=True, blank=True, on_delete=models.SET_NULL, related_name='audit_logs')

    def __str__(self):
        return f"{self.timestamp} - {self.user} - {self.action} - {self.model_name}({self.object_id})"
