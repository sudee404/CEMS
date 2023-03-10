# Generated by Django 4.1.7 on 2023-02-23 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index_app', '0011_event_host'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ['start_date'], 'verbose_name': 'Event', 'verbose_name_plural': 'Events'},
        ),
        migrations.AddField(
            model_name='event',
            name='approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='event',
            name='draft',
            field=models.BooleanField(default=True),
        ),
    ]
