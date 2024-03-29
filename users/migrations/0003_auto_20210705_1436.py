# Generated by Django 3.2.5 on 2021-07-05 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_rename_user_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='address1',
            field=models.CharField(blank=True, max_length=1024, null=True, verbose_name='Address line 1'),
        ),
        migrations.AddField(
            model_name='user',
            name='address2',
            field=models.CharField(blank=True, max_length=1024, null=True, verbose_name='Address line 2'),
        ),
        migrations.AddField(
            model_name='user',
            name='city',
            field=models.CharField(blank=True, max_length=1024, null=True, verbose_name='City'),
        ),
        migrations.AddField(
            model_name='user',
            name='description',
            field=models.TextField(blank=True, help_text="A little bit about yourself (don't be spammy)", max_length=4096, null=True, verbose_name='Description'),
        ),
        migrations.AddField(
            model_name='user',
            name='display_name',
            field=models.CharField(default='anonymous', help_text='Will be shown e.g. when commenting', max_length=30, verbose_name='Display name'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, max_length=17, null=True, verbose_name='Phone'),
        ),
        migrations.AddField(
            model_name='user',
            name='postal_code',
            field=models.CharField(blank=True, max_length=12, null=True, verbose_name='Postal Code'),
        ),
        migrations.AddField(
            model_name='user',
            name='website',
            field=models.URLField(blank=True, null=True, verbose_name='Website'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email'),
        ),
    ]
