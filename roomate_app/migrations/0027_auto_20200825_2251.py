# Generated by Django 3.1 on 2020-08-25 22:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roomate_app', '0026_auto_20200825_2242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apartment',
            name='token',
            field=models.CharField(max_length=100),
        ),
    ]
