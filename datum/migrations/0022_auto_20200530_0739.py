# Generated by Django 3.0.6 on 2020-05-30 14:39

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datum', '0021_auto_20200522_1043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customtag',
            name='text',
            field=ckeditor.fields.RichTextField(blank=True, verbose_name='Notes'),
        ),
    ]