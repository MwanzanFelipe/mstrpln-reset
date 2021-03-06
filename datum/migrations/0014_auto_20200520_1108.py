# Generated by Django 3.0.6 on 2020-05-20 18:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('datum', '0013_log'),
    ]

    operations = [
        migrations.AddField(
            model_name='log',
            name='Action',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='datum.Action'),
        ),
        migrations.AlterField(
            model_name='log',
            name='effort',
            field=models.IntegerField(choices=[(1, '1 - Hardly'), (2, '2'), (3, '3'), (4, '4'), (5, '5 - Very')], editable=False, verbose_name='Effort Level'),
        ),
        migrations.AlterField(
            model_name='log',
            name='enjoyment',
            field=models.IntegerField(choices=[(1, '1 - Hardly'), (2, '2'), (3, '3'), (4, '4'), (5, '5 - Very')], editable=False, verbose_name='Enjoyment'),
        ),
        migrations.AlterField(
            model_name='log',
            name='importance',
            field=models.IntegerField(choices=[(1, '1 - Hardly'), (2, '2'), (3, '3'), (4, '4'), (5, '5 - Very')], editable=False, verbose_name='Importance'),
        ),
        migrations.AlterField(
            model_name='log',
            name='relationship',
            field=models.IntegerField(choices=[(1, '1 - Hardly'), (2, '2'), (3, '3'), (4, '4'), (5, '5 - Very')], editable=False, verbose_name='Relationship'),
        ),
        migrations.AlterField(
            model_name='log',
            name='tags',
            field=models.CharField(blank=True, editable=False, max_length=200, verbose_name='Tags'),
        ),
        migrations.AlterField(
            model_name='log',
            name='title',
            field=models.CharField(editable=False, max_length=200, verbose_name='Title'),
        ),
    ]
