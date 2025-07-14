from django.shortcuts import render
from django.http import FileResponse
from pypdf import PdfReader, PdfWriter
import os
from django.core.files.storage import FileSystemStorage
from django.conf import settings

def index(request):
    return render(request, 'pdfapp/index.html')

from pypdf import PdfReader, PdfWriter

def merge_pdfs(request):
    if request.method == 'POST':
        files = request.FILES.getlist('pdfs')
        writer = PdfWriter()
        fs = FileSystemStorage()

        for f in files:
            filename = fs.save(f.name, f)
            filepath = fs.path(filename)
            reader = PdfReader(filepath)

            for page in reader.pages:
                writer.add_page(page)

        output_path = fs.path('merged.pdf')
        with open(output_path, 'wb') as f:
            writer.write(f)

        return FileResponse(open(output_path, 'rb'), as_attachment=True, filename='merged.pdf')
