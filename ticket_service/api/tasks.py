import os
import json
import requests
from base64 import b64encode

from celery import shared_task
from .models import Check


@shared_task
def html_to_pdf(id, order, type):
    url = 'http://wkhtmltopdf'
    encoding = 'utf-8'
    current_directory = os.path.dirname(os.path.abspath(__file__))
    pdf_directory = os.path.join(current_directory, "../media/pdf")
    path = f'ticket_service/media/pdf/{order["number"]}_{type}.pdf'

    with open('api/templates/input.html', 'r') as template_file:
        html_template = template_file.read()

    html_content = html_template.format(order['number'], order['data'])
    byte_content = html_content.encode()

    base64_bytes = b64encode(byte_content)
    base64_string = base64_bytes.decode(encoding)

    data = {
        'contents': base64_string,
    }
    headers = {
        'Content-Type': 'application/json',
    }
    response = requests.post(url, data=json.dumps(data), headers=headers)

    with open(f'{pdf_directory}/{order["number"]}_{type}.pdf', 'wb') as f:
        f.write(response.content)

    try:
        check_to_update = Check.objects.get(id=id)
        check_to_update.pdf_file = path
        check_to_update.status = 'rendered'
        check_to_update.save()
    except Check.DoesNotExist:
        return "File was generated, but not assigned to this check"

    return "File was create successfully"
