# Generated by Django 3.1.4 on 2021-02-08 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_categorydiscount'),
    ]

    operations = [
        migrations.AddField(
            model_name='categorydiscount',
            name='discount',
            field=models.DecimalField(blank=True, decimal_places=2, default=None, help_text='Enter discounts', max_digits=10, verbose_name='Скидка'),
            preserve_default=False,
        ),
    ]
