# Generated by Django 3.1 on 2020-08-19 02:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roomate_app', '0005_auto_20200819_0218'),
    ]

    operations = [
        migrations.AddField(
            model_name='apartment',
            name='token',
            field=models.CharField(default='5P7nBv1K1dIK77kMD-4HzA', max_length=100),
        ),
    ]
