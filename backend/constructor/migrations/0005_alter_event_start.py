# Generated by Django 3.2.5 on 2021-08-31 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('constructor', '0004_auto_20210830_1603'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='start',
            field=models.DateTimeField(verbose_name='Начало приема'),
        ),
    ]
