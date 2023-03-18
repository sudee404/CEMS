# Generated by Django 4.1.7 on 2023-03-18 04:51

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('index_app', '0014_guest_ticket'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='guest',
            options={'ordering': ['-event__start_date'], 'verbose_name': 'Guest', 'verbose_name_plural': 'Guests'},
        ),
        migrations.AddField(
            model_name='guest',
            name='qr_code',
            field=models.ImageField(default='default.png', upload_to='qr/'),
        ),
        migrations.AddField(
            model_name='guest',
            name='scanned',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='guest',
            name='ticket',
            field=models.UUIDField(default=uuid.uuid4, help_text='Unique ID for this particular ticket'),
        ),
    ]
