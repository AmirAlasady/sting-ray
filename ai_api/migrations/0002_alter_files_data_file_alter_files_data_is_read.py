# Generated by Django 5.0.6 on 2024-06-06 19:18

import ai_api.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ai_api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='files_data',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='uploads/', validators=[ai_api.models.validate_file_extension]),
        ),
        migrations.AlterField(
            model_name='files_data',
            name='is_read',
            field=models.CharField(choices=[('f', 'false'), ('t', 'true')], default='f', max_length=30),
        ),
    ]
