# Generated by Django 4.2.4 on 2023-09-04 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_check_pdf_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='check',
            name='pdf_file',
            field=models.FileField(blank=True, null=True, upload_to='ticket_service/media/pdf'),
        ),
    ]