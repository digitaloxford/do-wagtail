# Generated by Django 3.2 on 2021-06-03 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_auto_20210603_1353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='socialmediasettings',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
