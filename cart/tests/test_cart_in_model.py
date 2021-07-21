from django.shortcuts import redirect
from django.test import TestCase

from django.test.client import Client, RequestFactory
from django.urls import reverse

from cart.cart_in_session import CartInSession
from store.models import Product, CategoryDiscount
from test_unit_core.test_core import create_product_for_test, create_user


PROFILE_DETAIL_URL = redirect('store:index')