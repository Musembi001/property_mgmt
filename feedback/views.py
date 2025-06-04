from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Feedback
from .forms import FeedbackForm

@login_required
def feedback_list(request):
    feedbacks = Feedback.objects.all().order_by('-created_at')
    return render(request, "feedback/feedback_list.html", {"feedbacks": feedbacks})

@login_required
def feedback_submit(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            fb = form.save(commit=False)
            fb.user = request.user
            fb.save()
            return redirect('feedback_list')
    else:
        form = FeedbackForm()
    return render(request, "feedback/feedback_submit.html", {"form": form})
