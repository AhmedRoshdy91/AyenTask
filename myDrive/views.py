from django.shortcuts import render
from django.http import HttpResponse
from .forms import DocumentForm
from .models import Document
from django.db.models import Q

# Create your views here.


def upload(request):
    search = True
    default_form = DocumentForm()
    documents = Document.objects.all()
    if request.method == 'POST' and request.FILES['document']:
        if ".pdf" not in request.FILES['document'].name and ".ppt" not in request.FILES['document'].name:
            return render(request, 'files.html', {'form': default_form, "documents": documents, "search": search,
                                                  "error": "Invalid document"})
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

    return render(request, 'files.html', {'form': default_form, "documents": documents, "search": search})


def search(request):
    search = False
    doc = request.POST.get('doc_name')
    default_form = DocumentForm()
    documents = Document.objects.filter(
        Q(title__icontains=doc) | Q(document__icontains=doc)
    )
    return render(request, 'files.html', {'form': default_form, "documents": documents, "search": search})