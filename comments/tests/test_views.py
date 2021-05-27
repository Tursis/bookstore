from unittest import mock

from django.test import TestCase

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.test.client import Client
from django.urls import reverse