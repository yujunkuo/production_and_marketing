# Generated by Django 2.2.5 on 2019-12-25 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0016_auto_20191222_1619'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='oTime',
            field=models.DateTimeField(primary_key=True, serialize=False),
        ),
    ]