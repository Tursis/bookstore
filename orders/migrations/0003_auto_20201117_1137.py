# Generated by Django 3.1rc1 on 2020-11-17 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_auto_20201117_1135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='purchase_date',
            field=models.DateTimeField(verbose_name='Дата покупки'),
        ),
    ]
