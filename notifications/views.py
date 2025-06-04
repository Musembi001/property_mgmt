from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Notification

@login_required
def notifications_list(request):
    user = request.user
    notifications = Notification.objects.filter(user=user).order_by('-created_at')
    return render(request, "notifications/notifications_list.html", {"notifications": notifications})
