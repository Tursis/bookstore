# Generated by Django 3.1rc1 on 2020-11-02 13:57

import django.contrib.sessions.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sessions', '0001_initial'),
        ('store', '0001_initial'),
        ('cart', '0005_auto_20201021_1511'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartSession',
            fields=[
                ('session_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='sessions.session')),
                ('quantity', models.IntegerField(blank=True, default=0, help_text='Количество товара', null=True, verbose_name='Количество')),
                ('price', models.DecimalField(blank=True, decimal_places=2, default=0, help_text='Цена товара', max_digits=10, verbose_name='Цена')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.product', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'session',
                'verbose_name_plural': 'sessions',
                'abstract': False,
            },
            bases=('sessions.session',),
            managers=[
                ('objects', django.contrib.sessions.models.SessionManager()),
            ],
        ),
    ]
