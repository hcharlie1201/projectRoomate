# Generated by Django 3.1 on 2020-08-20 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roomate_app', '0006_apartment_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apartment',
            name='token',
            field=models.CharField(default='Sa3ZACIPlZ_f64NvTf7nTg', max_length=100),
        ),
    ]
