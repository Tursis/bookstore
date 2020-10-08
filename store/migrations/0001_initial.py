# Generated by Django 3.1rc1 on 2020-10-08 06:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BookAuthor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, help_text='Enter author name.', max_length=50, verbose_name='Имя')),
                ('slug', models.SlugField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='BookGenre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, help_text='Enter book genre.', max_length=50, verbose_name='Жанр')),
                ('slug', models.SlugField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, help_text='Enter book genre.', max_length=50, verbose_name='Жанр')),
                ('slug', models.SlugField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, help_text='Enter book name.', max_length=100, verbose_name='Название')),
                ('pages', models.CharField(blank=True, help_text='Enter number of pages', max_length=5, verbose_name='Количество страниц')),
                ('pub_year', models.IntegerField(blank=True, help_text='Enter year of publication', null=True, verbose_name='Год издания')),
                ('size', models.CharField(blank=True, help_text='Enter size book', max_length=10, verbose_name='Размеры')),
                ('price', models.DecimalField(blank=True, decimal_places=2, help_text='Enter price book', max_digits=10, verbose_name='Цена')),
                ('Discounts', models.DecimalField(blank=True, decimal_places=2, help_text='Enter discounts', max_digits=10, verbose_name='Скидка')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/books/', verbose_name='Изображение')),
                ('slug', models.SlugField(max_length=100)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.category')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, help_text='Enter book genre.', max_length=50, verbose_name='Жанр')),
                ('slug', models.SlugField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Magazine',
            fields=[
                ('product_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='store.product')),
                ('numb', models.IntegerField(blank=True, help_text='Enter number Magazine', null=True, verbose_name='Номер журнала')),
                ('numb_in_year', models.IntegerField(blank=True, help_text='Enter number Magazine', null=True, verbose_name='Номер журнала в году')),
                ('subs_price', models.DecimalField(blank=True, decimal_places=2, help_text='Enter price book', max_digits=10, null=True, verbose_name='Цена подписки')),
            ],
            bases=('store.product',),
        ),
        migrations.AddField(
            model_name='product',
            name='publisher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.publisher'),
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('product_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='store.product')),
                ('hard_cover', models.CharField(blank=True, help_text='Enter hard cover book (+/-)', max_length=1, verbose_name='Твердая обложка')),
                ('author', models.ManyToManyField(to='store.BookAuthor', verbose_name='Автор')),
                ('genre', models.ManyToManyField(to='store.BookGenre', verbose_name='Жанр')),
            ],
            bases=('store.product',),
        ),
    ]
