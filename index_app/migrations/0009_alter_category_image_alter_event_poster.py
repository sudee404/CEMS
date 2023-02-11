# Generated by Django 4.1.5 on 2023-02-09 22:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index_app', '0008_alter_category_image_alter_event_poster'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='image',
            field=models.ImageField(upload_to='images'),
        ),
        migrations.AlterField(
            model_name='event',
            name='poster',
            field=models.ImageField(upload_to='poster'),
        ),
    ]