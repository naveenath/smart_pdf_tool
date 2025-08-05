

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

def split_pdf(request):
    if request.method == 'POST':
        f = request.FILES['pdf']
        start = int(request.POST['start']) - 1
        end = int(request.POST['end'])

        fs = FileSystemStorage()
        filename = fs.save(f.name, f)
        file_path = fs.path(filename)

        reader = PdfReader(file_path)
        writer = PdfWriter()

        for page in range(start, end):
            writer.add_page(reader.pages[page])

        output_path = fs.path('split.pdf')
        with open(output_path, 'wb') as out:
            writer.write(out)

        return FileResponse(open(output_path, 'rb'), as_attachment=True, filename='split.pdf')

    if request.method == 'POST':
        f = request.FILES['pdf']
def extract_text(request):
    if request.method == 'POST':
        f = request.FILES['pdf']
        pages_input = request.POST.get('pages')  # optional, e.g., "1,3,5"

        fs = FileSystemStorage()
        filename = fs.save(f.name, f)
        file_path = fs.path(filename)

        reader = PdfReader(file_path)
        extracted_text = ""

        try:
            if pages_input:
                page_numbers = [int(p.strip()) - 1 for p in pages_input.split(',')]
            else:
                page_numbers = range(len(reader.pages))

            for page_num in page_numbers:
                if 0 <= page_num < len(reader.pages):
                    page = reader.pages[page_num]
                    extracted_text += page.extract_text() or ""
                    extracted_text += "\n\n--- Page Break ---\n\n"

        except Exception as e:
            return render(request, 'pdfapp/index.html', {'error': f"Error: {str(e)}"})

        # Save to a .txt file
        output_path = fs.path('extracted_text.txt')
        with open(output_path, 'w', encoding='utf-8') as out:
            out.write(extracted_text)

        return FileResponse(open(output_path, 'rb'), as_attachment=True, filename='extracted_text.txt')
