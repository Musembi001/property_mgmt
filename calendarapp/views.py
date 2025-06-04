from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Event
from .forms import EventForm
from django.db import models

@login_required
def event_list(request):
    user = request.user
    if hasattr(user, "role"):
        if user.role == "tenant":
            # Show events relevant to this tenant (e.g., events for their property/unit or created by them)
            events = Event.objects.filter(
                models.Q(created_by=user) | models.Q(property__unit__lease__tenant=user)
            ).distinct().order_by('start_time')
        elif user.role == "landlord":
            # Show events for properties owned by landlord or created by them
            events = Event.objects.filter(
                models.Q(created_by=user) | models.Q(property__landlord=user)
            ).distinct().order_by('start_time')
        elif user.role == "agent":
            # Show events for properties managed by agent or created by them
            events = Event.objects.filter(
                models.Q(created_by=user) | models.Q(property__agent=user)
            ).distinct().order_by('start_time')
        elif user.role == "caretaker":
            # Show events for properties managed by caretaker or created by them
            events = Event.objects.filter(
                models.Q(created_by=user) | models.Q(property__caretaker=user)
            ).distinct().order_by('start_time')
        else:
            events = Event.objects.filter(created_by=user).order_by('start_time')
    else:
        events = Event.objects.filter(created_by=user).order_by('start_time')
    return render(request, "calendarapp/event_list.html", {"events": events})

@login_required
def event_create(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, "calendarapp/event_create.html", {"form": form})

@login_required
def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    # Optionally restrict access to only allowed users
    return render(request, "calendarapp/event_detail.html", {"event": event})
