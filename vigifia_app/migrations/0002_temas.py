# Generated by Django 5.1.2 on 2024-11-07 23:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vigifia_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Temas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tema', models.CharField(max_length=100)),
                ('titulo', models.CharField(max_length=200)),
                ('region', models.CharField(max_length=100)),
                ('info', models.CharField(max_length=600)),
            ],
        ),
    ]
