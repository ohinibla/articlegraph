# Generated by Django 3.2.2 on 2021-06-26 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('graph', '0003_site_thumb_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='site',
            name='thumb_img',
            field=models.URLField(default=''),
        ),
    ]
