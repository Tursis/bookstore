# Generated by Django 3.1.4 on 2021-03-19 12:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('store', '0010_auto_20210319_1419'),
    ]

    operations = [
        migrations.CreateModel(
            name='ViewStatistics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(blank=True, null=True, verbose_name='Количество просмотров')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.product', verbose_name='Товар')),
            ],
        ),
    ]