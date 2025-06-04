from django.db import models
from django.contrib.auth import get_user_model

class Feedback(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True)
    message = models.TextField()
    rating = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)], null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    response = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Feedback from {self.user} on {self.created_at:%Y-%m-%d}"
