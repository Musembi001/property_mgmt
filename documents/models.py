from django.db import models
from django.contrib.auth import get_user_model
from properties.models import Building  # or Property if that's your model name

class Document(models.Model):
    DOCUMENT_TYPE_CHOICES = [
        ('rules', 'Rules'),
        ('notice', 'Notice'),
        ('manual', 'Manual'),
        ('other', 'Other'),
    ]
    title = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=DOCUMENT_TYPE_CHOICES, default='other')
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='documents/')
    uploaded_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    property = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='documents', null=True, blank=True)

    def __str__(self):
        return self.title
