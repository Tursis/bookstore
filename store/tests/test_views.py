from unittest import mock

from django.test import TestCase
from django.contrib.auth.models import User
from django.test.client import RequestFactory

from django.urls import reverse

from comments.models import ProductReviews
from shared.permissions import PERMISSION_ON_SITE, permission_for_user
from store.models import Product, Book
from test_unit_core.test_core import create_product_for_test, create_user


class ProductListViewTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        create_user('Tursis', '123456', 'test@gmail.com')
        create_product_for_test(2)

    def tearDown(self):
        for item in Product.objects.all():
            item.image.delete()

    def test_index_template(self):
        resp = self.client.get(reverse('store:index'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'index.html')

    @mock.patch('store.views.ProductFilter')
    def test_call_product_filter(self, mock_product_filter):
        resp = self.client.get(reverse('store:index'))
        mock_product_filter.assert_called()

    @mock.patch('store.views.product_filter_counter')
    def test_call_product_filter_counter(self, mock_product_filter_counter):
        resp = self.client.get(reverse('store:index'))
        mock_product_filter_counter.assert_called()

    @mock.patch('store.views.update_model_counter')
    def test_call_update_model_counter(self, mock_update_model_counter):
        resp = self.client.get(reverse('store:index'))
        mock_update_model_counter.assert_called()


class BooksDetailView(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        create_user('Tursis', '123456', 'test@gmail.com')
        create_product_for_test(2)

    def tearDown(self):
        for item in Product.objects.all():
            item.image.delete()

    def test_book_detail_template(self):
        product = Product.objects.get(pk=1)
        resp = self.client.get(reverse('store:book_detail', args=[product, ]))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'store/book/book_detail.html')

    @mock.patch('store.views.quantity_reviews')
    def test_called_quantity_reviews(self, mock_quantity_reviews):
        product = Product.objects.get(pk=1)
        resp = self.client.get(reverse('store:book_detail', args=[product, ]))
        mock_quantity_reviews.assert_called()

    def test_product_reviews_form_in_context(self):
        product = Product.objects.get(pk=1)
        ProductReviews.objects.create(user=User.objects.get(pk=1), product=product, description='reviews', rating=4,
                                      active=True)
        resp = self.client.get(reverse('store:book_detail', args=[product, ]))
        self.assertTrue(resp.context['reviews_list'])

    def test_review_comment_form_in_context(self):
        product = Product.objects.get(pk=1)
        resp = self.client.get(reverse('store:book_detail', args=[product, ]))
        self.assertTrue(resp.context['comment_form'])

    @mock.patch('store.views.ReviewCommentView')
    def test_called_review_comment_view(self, mock_review_comment_view):
        product = Product.objects.get(pk=1)
        resp = self.client.post(reverse('store:book_detail', args=[product, ]))
        mock_review_comment_view.post.assert_called()


class ProductManageViewTest(TestCase):

    def setUp(self):
        create_user('Tursis', '123456', 'test@gmail.com')
        user = User.objects.get(pk=1)
        user.is_superuser = True
        user.save()

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('store:product_manage'))
        self.assertRedirects(resp, '/accounts/login/?next=/store/manage/')

    def test_logged_in_user_correct_template(self):
        login = self.client.login(username='Tursis', password='123456')
        resp = self.client.get(reverse('store:product_manage'))
        self.assertTrue(login)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'store/product_manage.html')


class BooksManagerViewTest(TestCase):

    def setUp(self):
        create_user('Tursis', '123456', 'test@gmail.com')
        create_user('test_user', '123456', 'test@gmail.com')
        user = User.objects.get(pk=1)
        for moderator_permission in PERMISSION_ON_SITE['moderator']:
            user.user_permissions.add(permission_for_user(moderator_permission))
            user.save()

    def test_book_manager_template_permission_required_user(self):
        login = self.client.login(username='test_user', password='123456')
        resp = self.client.get(reverse('store:book_manage'))
        self.assertTrue(login)
        self.assertEqual(resp.status_code, 403)

    def test_book_manager_template_permission_required_moderator(self):
        login = self.client.login(username='Tursis', password='123456')
        resp = self.client.get(reverse('store:book_manage'))
        self.assertTrue(login)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'store/book/book_manage.html')


class BooksCRUDTest(TestCase):

    def setUp(self):
        create_product_for_test(2)
        create_user('Tursis', '123456', 'test@gmail.com')
        create_user('test_user', '123456', 'test2@gmail.com')
        user = User.objects.get(pk=1)
        for moderator_permission in PERMISSION_ON_SITE['moderator']:
            user.user_permissions.add(permission_for_user(moderator_permission))
            user.save()

    def test_book_create_template_permission_required_user(self):
        login = self.client.login(username='test_user', password='123456')
        resp = self.client.get(reverse('store:book_create'))
        self.assertTrue(login)
        self.assertEqual(resp.status_code, 403)

    def test_book_create_template_permission_required_moderator(self):
        login = self.client.login(username='Tursis', password='123456')
        resp = self.client.get(reverse('store:book_create'))
        self.assertTrue(login)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'store/book/book_create.html')

    def test_book_update_template_permission_required_user(self):
        product = Product.objects.get(pk=1)
        login = self.client.login(username='test_user', password='123456')
        resp = self.client.get(reverse('store:book_update', args=(product,)))
        self.assertTrue(login)
        self.assertEqual(resp.status_code, 403)

    def test_book_update_template_permission_required_moderator(self):
        product = Product.objects.get(pk=1)
        login = self.client.login(username='Tursis', password='123456')
        resp = self.client.get(reverse('store:book_update', args=(product,)))
        self.assertTrue(login)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'store/book/book_update.html')

    def test_book_delete_template_permission_required_user(self):
        product = Product.objects.get(pk=1)
        login = self.client.login(username='test_user', password='123456')
        resp = self.client.get(reverse('store:book_delete', args=(product, )))
        self.assertTrue(login)
        self.assertEqual(resp.status_code, 403)

    def test_book_delete_template_permission_required_moderator(self):
        product = Product.objects.get(pk=1)
        login = self.client.login(username='Tursis', password='123456')
        resp = self.client.get(reverse('store:book_delete', args=(product, )))
        self.assertTrue(login)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'store/book/book_delete.html')


class MagazineCRUDTest(TestCase):

    def setUp(self):
        create_product_for_test(2)
        create_user('Tursis', '123456', 'test@gmail.com')
        create_user('test_user', '123456', 'test2@gmail.com')
        user = User.objects.get(pk=1)
        for moderator_permission in PERMISSION_ON_SITE['moderator']:
            user.user_permissions.add(permission_for_user(moderator_permission))
            user.save()

    def test_magazine_create_template_permission_required_user(self):
        login = self.client.login(username='test_user', password='123456')
        resp = self.client.get(reverse('store:magazine_create'))
        self.assertTrue(login)
        self.assertEqual(resp.status_code, 403)

    def test_magazine_create_template_permission_required_moderator(self):
        login = self.client.login(username='Tursis', password='123456')
        resp = self.client.get(reverse('store:magazine_create'))
        self.assertTrue(login)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'store/magazine/magazine_create.html')

    def test_magazine_update_template_permission_required_user(self):
        product = Product.objects.get(pk=3)
        login = self.client.login(username='test_user', password='123456')
        resp = self.client.get(reverse('store:magazine_update', args=(product,)))
        self.assertTrue(login)
        self.assertEqual(resp.status_code, 403)

    def test_magazine_update_template_permission_required_moderator(self):
        product = Product.objects.get(pk=3)
        login = self.client.login(username='Tursis', password='123456')
        resp = self.client.get(reverse('store:magazine_update', args=(product,)))
        self.assertTrue(login)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'store/magazine/magazine_update.html')

    def test_magazine_delete_template_permission_required_user(self):
        product = Product.objects.get(pk=3)
        login = self.client.login(username='test_user', password='123456')
        resp = self.client.get(reverse('store:magazine_delete', args=(product, )))
        self.assertTrue(login)
        self.assertEqual(resp.status_code, 403)

    def test_magazine_delete_template_permission_required_moderator(self):
        product = Product.objects.get(pk=3)
        login = self.client.login(username='Tursis', password='123456')
        resp = self.client.get(reverse('store:magazine_delete', args=(product, )))
        self.assertTrue(login)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'store/magazine/magazine_delete.html')
