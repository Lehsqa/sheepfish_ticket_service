import os
import zipfile

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
from .models import Printer, Check
from .serializers import CheckSerializer
from .tasks import html_to_pdf


@api_view(['POST'])
def check_create(request):
    if request.method == 'POST':
        try:
            data = request.data
            printer = Printer.objects.get(api_key=data['api_key'])
            try:
                check = Check.objects.get(order=data['order'], type=printer.check_type)
                if data['order']['number'] == check.order['number']:
                    return Response("Check already exist", status=status.HTTP_400_BAD_REQUEST)
            except Check.DoesNotExist:
                pass
            data['printer_id'] = printer.id
            data['type'] = printer.check_type
            data['status'] = 'new'

            serializer = CheckSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                html_to_pdf.delay(serializer.data['id'], data['order'], printer.check_type)
                return Response("Check was create successfully", status=status.HTTP_201_CREATED)
            return Response("Invalid validation", status=status.HTTP_400_BAD_REQUEST)
        except Printer.DoesNotExist:
            return Response("Printer doesn't exist", status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def check_download(request):
    if request.method == 'GET':
        try:
            printer = Printer.objects.get(api_key=request.GET.get('api_key'))
            checks = Check.objects.filter(printer_id=printer).exclude(status='printed')
        except Printer.DoesNotExist:
            return Response("Api key isn't correct or empty", status=status.HTTP_400_BAD_REQUEST)
        zip_filename = "checks.zip"

        if len(checks) == 0:
            return Response("Rendered checks don't exist", status=status.HTTP_200_OK)
        elif len(checks) == 1:
            file_name = os.path.basename(checks[0].pdf_file.file.name)
            response = HttpResponse(checks[0].pdf_file.file, content_type='application/force-download')
            response['Content-Disposition'] = f'attachment; filename="{file_name}"'
        else:
            with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for check in checks:
                    file_name = os.path.basename(check.pdf_file.file.name)
                    zipf.write(check.pdf_file.file.name, arcname=file_name)

            response = HttpResponse(open(zip_filename, 'rb').read(), content_type='application/zip')
            response['Content-Disposition'] = f'attachment; filename="{zip_filename}"'
            os.remove(zip_filename)

        checks.update(status='printed')
        return response
