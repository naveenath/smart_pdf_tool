from django.shortcuts import render
from django.http import FileResponse
from pypdf import PdfReader, PdfWriter
import os
from django.core.files.storage import FileSystemStorage
from django.conf import settings

# Renders the main index page with the upload form
def index(request):
    return render(request, 'pdfapp/index.html')


def merge_pdfs(request):
    if request.method == 'POST':
        files = request.FILES.getlist('pdfs')  # Get list of uploaded PDF files
        writer = PdfWriter()
        fs = FileSystemStorage()

        for f in files:
            filename = fs.save(f.name, f)  # Save each file to the server
            filepath = fs.path(filename)   # Get the path of the saved file
            reader = PdfReader(filepath)

            # Add all pages from this PDF to the writer
            for page in reader.pages:
                writer.add_page(page)

        output_path = fs.path('merged.pdf')  # Static name — should be made unique
        with open(output_path, 'wb') as f:
            writer.write(f)  # Write merged PDF to disk

        # Return the file as a downloadable response
        return FileResponse(open(output_path, 'rb'), as_attachment=True, filename='merged.pdf')


def split_pdf(request):
    if request.method == 'POST':
        f = request.FILES['pdf']  # Get the uploaded file
        start = int(request.POST['start']) - 1  # Page indices are 0-based
        end = int(request.POST['end'])

        fs = FileSystemStorage()
        filename = fs.save(f.name, f)
        file_path = fs.path(filename)

        reader = PdfReader(file_path)
        writer = PdfWriter()

        # Extract pages in the specified range
        for page in range(start, end):
            writer.add_page(reader.pages[page])

        output_path = fs.path('split.pdf')  # Static name — should be made unique
        with open(output_path, 'wb') as out:
            writer.write(out)

        return FileResponse(open(output_path, 'rb'), as_attachment=True, filename='split.pdf')

    # ❌ This block is redundant and has no effect — should be removed
    if request.method == 'POST':
        f = request.FILES['pdf']


def extract_text(request):
    if request.method == 'POST':
        f = request.FILES['pdf']  # Uploaded PDF file
        pages_input = request.POST.get('pages')  # Optional input like "1,3,5"

        fs = FileSystemStorage()
        filename = fs.save(f.name, f)
        file_path = fs.path(filename)

        reader = PdfReader(file_path)
        extracted_text = ""

        try:
            # Parse page numbers from the input, default to all pages if not provided
            if pages_input:
                page_numbers = [int(p.strip()) - 1 for p in pages_input.split(',')]
            else:
                page_numbers = range(len(reader.pages))

            # Extract text from each requested page
            for page_num in page_numbers:
                if 0 <= page_num < len(reader.pages):
                    page = reader.pages[page_num]
                    extracted_text += f"\n\n--- Page {page_num + 1} ---\n\n"  # Optional enhancement
                    extracted_text += page.extract_text() or ""
                    extracted_text += "\n\n--- Page Break ---\n\n"

        except Exception as e:
            # Handle invalid input or extraction error
            return render(request, 'pdfapp/index.html', {'error': f"Error: {str(e)}"})

        # Save the extracted text to a file
        output_path = fs.path('extracted_text.txt')  # Static name — should be made unique
        with open(output_path, 'w', encoding='utf-8') as out:
            out.write(extracted_text)

        return FileResponse(open(output_path, 'rb'), as_attachment=True, filename='extracted_text.txt')
