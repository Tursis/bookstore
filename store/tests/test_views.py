from django.test import TestCase
from django.contrib.auth.models import User

from store.models import Product, Book, Magazine, Category, Publisher, BookAuthor, BookGenre
from django.urls import reverse


class ProductListViewTest(TestCase):

    @classmethod
    def SetUpTestData(cls):
        number = 13
        [Category.objects.create(name=category_item) for category_item in range(1, 3)]
        [Publisher.objects.create(name=publisher_item) for publisher_item in range(1, number)]
        [BookAuthor.objects.create(name=author_item) for author_item in range(1, number)]
        [BookGenre.objects.create(name=genre_item) for genre_item in range(1, number)]

        for product_item in range(1, number):
            Book.objects.create(category=Category.objects.get(pk=1), name='book_%s' % product_item,
                                publisher=Publisher.objects.get(pk=product_item),
                                price=product_item * 10, Discounts=0, hard_cover='+', pages=5 * product_item,
                                pub_year=2000 + product_item, size='240x165'
                                )

            Book.objects.get(pk=product_item).author.add(BookAuthor.objects.get(pk=product_item))
            Book.objects.get(pk=product_item).genre.add(BookGenre.objects.get(pk=product_item))

        for product_item in range(1, number):
            Magazine.objects.create(category=Category.objects.get(pk=2), name='magazine_%s' % product_item,
                                    publisher=Publisher.objects.get(pk=product_item),
                                    price=product_item * 10, Discounts=0, numb=product_item, numb_in_year=product_item,
                                    subs_price=20 * product_item, pages=5 * product_item,
                                    pub_year=2000 + product_item, size='240x165')

    def test_get_response(self):
        resp = self.client.get('index.html')
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('store:index'))
        self.assertEqual(resp.status_code, 200)

        self.assertTemplateUsed(resp, 'index.html')


class AuthorizationСheckTest(TestCase):

    def setUp(self):
        test_user = User.objects.create_user(username='admin')
        test_user.set_password('admin')
        test_user.is_superuser = True
        test_user.save()

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('store:product_manage'))
        self.assertRedirects(resp, '/accounts/login/?next=/store/manage/')

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='admin', password='admin')
        resp = self.client.get(reverse('store:product_manage'))

        self.assertTrue(login)
        self.assertEqual(resp.status_code, 200)

        # Проверка того, что мы используем правильный шаблон
        self.assertTemplateUsed(resp, 'store/product_manage.html')
