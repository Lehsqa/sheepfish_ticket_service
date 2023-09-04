from django.db import models


CHECK_TYPE = (
    ('kitchen', 'Kitchen'),
    ('client', 'Client'),
)

STATUS = (
    ('new', 'New'),
    ('rendered', 'Rendered'),
    ('printed', 'Printed'),
)


class Printer(models.Model):
    name = models.CharField(max_length=100)
    api_key = models.CharField(max_length=100)
    check_type = models.CharField(choices=CHECK_TYPE, max_length=7)
    point_id = models.IntegerField()


class Check(models.Model):
    printer_id = models.ForeignKey(Printer, on_delete=models.CASCADE)
    type = models.CharField(choices=CHECK_TYPE, max_length=7)
    order = models.JSONField()
    status = models.CharField(choices=STATUS, max_length=8)
    pdf_file = models.FileField(upload_to='./ticket_service/media/pdf', blank=True, null=True)
