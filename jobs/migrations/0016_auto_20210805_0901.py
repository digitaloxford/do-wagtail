# Generated by Django 3.2.6 on 2021-08-05 09:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('jobs', '0015_alter_recruiterpage_user_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recruiterpage',
            name='user_id',
        ),
        migrations.AddField(
            model_name='recruiterpage',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
