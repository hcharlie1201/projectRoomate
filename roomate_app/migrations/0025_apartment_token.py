# Generated by Django 3.1 on 2020-08-25 22:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roomate_app', '0024_remove_apartment_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='apartment',
            name='token',
            field=models.CharField(default='4d266a75a45a9abd7870f8aa3487aac74ba55eeb', max_length=100),
        ),
    ]
