from django.db import models
from django.contrib.auth import get_user_model

class Notification(models.Model):
    CHANNEL_CHOICES = [
        ('inapp', 'In-App'),
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('whatsapp', 'WhatsApp'),
    ]
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    channel = models.CharField(max_length=20, choices=CHANNEL_CHOICES, default='inapp')
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    sent = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} - {self.channel} - {self.message[:30]}"
