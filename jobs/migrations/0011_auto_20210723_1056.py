# Generated by Django 3.2.5 on 2021-07-23 10:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0010_auto_20210723_1039'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recruiterpage',
            name='address1',
        ),
        migrations.RemoveField(
            model_name='recruiterpage',
            name='address2',
        ),
        migrations.RemoveField(
            model_name='recruiterpage',
            name='city',
        ),
        migrations.RemoveField(
            model_name='recruiterpage',
            name='description',
        ),
        migrations.RemoveField(
            model_name='recruiterpage',
            name='display_name',
        ),
        migrations.RemoveField(
            model_name='recruiterpage',
            name='email',
        ),
        migrations.RemoveField(
            model_name='recruiterpage',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='recruiterpage',
            name='postal_code',
        ),
        migrations.RemoveField(
            model_name='recruiterpage',
            name='user_id',
        ),
        migrations.RemoveField(
            model_name='recruiterpage',
            name='website',
        ),
    ]
