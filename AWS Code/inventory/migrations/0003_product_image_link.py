# Generated by Django 5.0.6 on 2024-07-08 03:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("inventory", "0002_userprofile_vendor"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="image_link",
            field=models.URLField(blank=True, max_length=1024, null=True),
        ),
    ]
