# Generated by Django 5.0.3 on 2024-06-03 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_manager'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotel',
            name='address',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='hotel',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='hotel',
            name='image',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
