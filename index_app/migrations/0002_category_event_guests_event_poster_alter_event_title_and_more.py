# Generated by Django 4.1.5 on 2023-02-09 21:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('index_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('image', models.ImageField(height_field=500, upload_to='image', width_field=500)),
                ('description', models.TextField()),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.AddField(
            model_name='event',
            name='guests',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='poster',
            field=models.ImageField(default='default.png', height_field=1400, max_length=800, upload_to='poster', width_field=700),
        ),
        migrations.AlterField(
            model_name='event',
            name='title',
            field=models.CharField(max_length=250),
        ),
        migrations.AddField(
            model_name='event',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='index_app.category'),
        ),
    ]
