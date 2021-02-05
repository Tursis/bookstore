# Generated by Django 3.1.4 on 2021-02-05 12:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0004_delete_productcomment'),
        ('comments', '0003_auto_20210201_1052'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductReviews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(help_text='Enter your comment here', max_length=400, verbose_name='Коментарий')),
                ('rating', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], help_text='Enter rating here', verbose_name='Оценка')),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=True, verbose_name='активация коментария')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.product')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['pub_date'],
            },
        ),
        migrations.DeleteModel(
            name='ProductComment',
        ),
    ]
