from django.db import models
from django.contrib.auth import get_user_model
from properties.models import Building  # or Property if that's your model name

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    property = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='events', null=True, blank=True)

    def __str__(self):
        return self.title
