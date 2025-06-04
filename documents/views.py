from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Document
from .forms import DocumentForm

@login_required
def document_list(request):
    user = request.user
    if hasattr(user, "role"):
        if user.role == "tenant":
            # Show documents for properties where this tenant has a lease
            from leases.models import Lease
            property_ids = Lease.objects.filter(tenant=user).values_list('unit__building_id', flat=True)
            documents = Document.objects.filter(property_id__in=property_ids).order_by('-uploaded_at')
        elif user.role == "caretaker":
            # Show documents for properties this caretaker manages
            property_ids = user.caretaker_buildings.values_list('id', flat=True)
            documents = Document.objects.filter(property_id__in=property_ids).order_by('-uploaded_at')
        elif user.role == "agent":
            # Show documents for properties this agent manages
            property_ids = user.agent_buildings.values_list('id', flat=True)
            documents = Document.objects.filter(property_id__in=property_ids).order_by('-uploaded_at')
        elif user.role == "landlord":
            # Show documents for properties owned by landlord
            property_ids = user.building_set.values_list('id', flat=True)
            documents = Document.objects.filter(property_id__in=property_ids).order_by('-uploaded_at')
        else:
            documents = Document.objects.none()
    else:
        documents = Document.objects.none()

    doc_type = request.GET.get('type')
    if doc_type:
        documents = documents.filter(type=doc_type)

    return render(request, "documents/document_list.html", {"documents": documents})

@login_required
def document_upload(request):
    if not hasattr(request.user, "role") or request.user.role == "tenant":
        return redirect('document_list')  # or show a permission denied message
    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.uploaded_by = request.user
            doc.save()
            return redirect('document_list')
    else:
        form = DocumentForm()
    return render(request, "documents/document_upload.html", {"form": form})

@login_required
def document_detail(request, pk):
    document = get_object_or_404(Document, pk=pk)
    # Optionally restrict access to only allowed users
    return render(request, "documents/document_detail.html", {"document": document})
