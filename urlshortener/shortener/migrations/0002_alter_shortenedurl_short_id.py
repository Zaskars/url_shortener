# Generated by Django 5.0.1 on 2024-01-28 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shortener", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="shortenedurl",
            name="short_id",
            field=models.CharField(max_length=8, unique=True),
        ),
    ]
