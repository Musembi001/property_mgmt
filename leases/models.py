from django.db import models
from accounts.models import User
from properties.models import Unit

class Lease(models.Model):
    tenant = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'tenant'})
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    rent_amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Lease: {self.tenant} - {self.unit}"
