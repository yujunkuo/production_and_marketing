# Generated by Django 3.0.1 on 2020-01-01 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0005_auto_20191228_0344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='oTime',
            field=models.DateTimeField(),
        ),
    ]
