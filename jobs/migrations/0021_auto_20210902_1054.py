# Generated by Django 3.2.6 on 2021-09-02 10:54

from django.db import migrations, models
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0020_jobpage_short_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobpage',
            name='closing_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='jobpage',
            name='description',
            field=wagtail.fields.RichTextField(),
        ),
        migrations.AlterField(
            model_name='jobpage',
            name='job_link',
            field=models.URLField(default='https://example.com'),
            preserve_default=False,
        ),
    ]
