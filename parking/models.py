from django.db import models
from django.contrib.auth import get_user_model
from properties.models import Building  # or Property

class ParkingSlot(models.Model):
    slot_number = models.CharField(max_length=20, unique=True)
    location = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    property = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='parking_slots', null=True, blank=True)  # Add this

    def __str__(self):
        return f"Slot {self.slot_number} ({'Active' if self.is_active else 'Inactive'})"

class ParkingAssignment(models.Model):
    slot = models.ForeignKey(ParkingSlot, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    assigned_at = models.DateTimeField(auto_now_add=True)
    valid_until = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.slot} assigned to {self.user}"