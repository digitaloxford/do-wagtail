# Generated by Django 3.2.5 on 2021-07-05 14:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0008_auto_20210705_1436'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobpage',
            name='recruiter',
        ),
    ]