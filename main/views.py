from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
import os
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from . import models
from pdf2docx import parse
from docx2pdf import convert


def upload_pdf(request):
    if request.method == 'POST':
        pdf_file = request.FILES.get('file')
        if pdf_file:
            # Faylni media papkasiga saqlash
            fs = FileSystemStorage()
            pdf_filename = fs.save(pdf_file.name, pdf_file)
            pdf_filepath = fs.path(pdf_filename)

            # docx fayl nomini aniqlash
            docx_filename = os.path.splitext(pdf_filename)[0] + '.docx'
            docx_filepath = os.path.join(settings.MEDIA_ROOT, docx_filename)

            # PDFni DOCXga konvertatsiya qilish
            parse(pdf_filepath, docx_filepath)

            # Faylni modelga saqlash
            file = models.File.objects.create(file=docx_filename)
            return redirect('download_word', file.id)

    return render(request, 'pdf/upload.html')


def download_word(request, id):
    file = get_object_or_404(models.File, id=id)
    file_path = os.path.join(settings.MEDIA_ROOT, file.file.name)

    if os.path.exists(file_path):
        # Faylni o'qish
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(),
                                    content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)

        # Faylni modeldan o'chirish
        file.delete()
        # Faylni fayl tizimidan o'chirish
        os.remove(file_path)
        return response
    else:
        return HttpResponse("File not found.", status=404)


def upload_word(request):
    if request.method == 'POST':
        word_file = request.FILES.get('file')
        if word_file:
            # Faylni media papkasiga saqlash
            fs = FileSystemStorage()
            word_filename = fs.save(word_file.name, word_file)
            word_filepath = fs.path(word_filename)

            # DOCX fayl nomini aniqlash
            pdf_filename = os.path.splitext(word_filename)[0] + '.pdf'
            pdf_filepath = os.path.join(settings.MEDIA_ROOT, pdf_filename)

            # DOCXni PDFga konvertatsiya qilish
            convert(word_filepath, pdf_filepath)

            # Faylni modelga saqlash
            file = models.File.objects.create(file=pdf_filename)
            return redirect('download_pdf', file.id)

    return render(request, 'word/upload.html')


def download_pdf(request, id):
    file = get_object_or_404(models.File, id=id)
    file_path = os.path.join(settings.MEDIA_ROOT, file.file.name)

    if os.path.exists(file_path):
        # Faylni o'qish
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/pdf")
            response['Content-Disposition'] = f'attachment; filename={os.path.basename(file_path)}'
        # Faylni modeldan o'chirish
        file.delete()
        # Faylni fayl tizimidan o'chirish
        os.remove(file_path)
        return response
    else:
        return HttpResponse("File not found.", status=404)
