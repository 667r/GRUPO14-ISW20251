# Generated by Django 5.1.2 on 2025-05-05 00:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vigifia_app', '0008_fuenteexterna'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fuenteexterna',
            name='archivo_csv',
            field=models.FileField(blank=True, null=True, upload_to='fuentes/'),
        ),
    ]
