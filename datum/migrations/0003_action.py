# Generated by Django 3.0.6 on 2020-05-17 19:57

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('datum', '0002_auto_20200517_0718'),
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('postit_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='datum.PostIt')),
                ('effort', models.IntegerField(choices=[(1, '1 - Hardly'), (2, '2'), (3, '3'), (4, '4'), (5, '5 - Very')], default=3, verbose_name='Effort Level')),
                ('importance', models.IntegerField(choices=[(1, '1 - Hardly'), (2, '2'), (3, '3'), (4, '4'), (5, '5 - Very')], default=3, verbose_name='Importance')),
                ('enjoyment', models.IntegerField(choices=[(1, '1 - Hardly'), (2, '2'), (3, '3'), (4, '4'), (5, '5 - Very')], default=3, verbose_name='Enjoyment')),
                ('relationship', models.IntegerField(choices=[(1, '1 - Hardly'), (2, '2'), (3, '3'), (4, '4'), (5, '5 - Very')], default=3, verbose_name='Relationship')),
                ('priority', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, verbose_name='Priority Level')),
                ('complete', models.BooleanField(default=False, verbose_name='Completion Status')),
                ('starred', models.BooleanField(default=False, verbose_name='Star Status')),
                ('last_modified', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Last Modified')),
                ('tags', models.CharField(blank=True, max_length=200, verbose_name='Tags')),
                ('due_date', models.DateField(blank=True, null=True, verbose_name='Due Date')),
                ('snooze_date', models.DateField(blank=True, null=True, verbose_name='Snooze Date')),
                ('recurrence_date', models.DateField(blank=True, null=True, verbose_name='Recurrence Date')),
                ('recreation_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Recreation DateTime')),
            ],
            options={
                'verbose_name': 'Next Action',
                'ordering': ['-priority', 'title'],
            },
            bases=('datum.postit',),
        ),
    ]
