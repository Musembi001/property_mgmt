from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from .models import AuditLog
from properties.models import Building

def get_request_user():
    # Placeholder: You need a way to get the current request user (see below)
    return None

@receiver(post_save)
def log_model_save(sender, instance, created, **kwargs):
    # Only log for your project apps, not Django built-ins
    if sender._meta.app_label in ['leases', 'properties', 'payments', 'maintenance']:
        action = 'create' if created else 'update'
        user = getattr(instance, '_audit_user', None) or get_request_user()
        AuditLog.objects.create(
            user=user,
            action=action,
            model_name=sender.__name__,
            object_id=str(instance.pk),
            object_repr=str(instance),
            property=getattr(instance, 'building', None) or getattr(instance, 'property', None)
        )

@receiver(post_delete)
def log_model_delete(sender, instance, **kwargs):
    if sender._meta.app_label in ['leases', 'properties', 'payments', 'maintenance']:
        user = getattr(instance, '_audit_user', None) or get_request_user()
        AuditLog.objects.create(
            user=user,
            action='delete',
            model_name=sender.__name__,
            object_id=str(instance.pk),
            object_repr=str(instance),
            property=getattr(instance, 'building', None) or getattr(instance, 'property', None)
        )