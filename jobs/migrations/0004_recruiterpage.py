# Generated by Django 3.2.4 on 2021-06-21 19:56

from django.db import migrations, models
import django.db.models.deletion
import wagtail.fields
import wagtailmetadata.models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0062_comment_models_and_pagesubscription'),
        ('wagtailimages', '0023_add_choose_permissions'),
        ('jobs', '0003_auto_20210621_1937'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecruiterPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('description', wagtail.fields.RichTextField(blank=True)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=50)),
                ('address_address1', models.CharField(max_length=200)),
                ('address_address2', models.CharField(blank=True, max_length=200, null=True)),
                ('address_city', models.CharField(max_length=100)),
                ('address_postcode', models.CharField(max_length=10)),
                ('search_image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image', verbose_name='Search image')),
            ],
            options={
                'ordering': ['title'],
            },
            bases=(wagtailmetadata.models.WagtailImageMetadataMixin, 'wagtailcore.page', models.Model),
        ),
    ]
