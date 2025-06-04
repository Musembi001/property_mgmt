from django.db import models
from properties.models import Unit
from accounts.models import User

class MaintenanceRequest(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    description = models.TextField()
    requested_by = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[('open', 'Open'), ('in_progress', 'In Progress'), ('closed', 'Closed')], default='open')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request for {self.unit} - {self.status}"
