# Create your tests here.
import json

from django.conf import settings
from django.test import RequestFactory, TestCase
import pytest

@pytest.fixture(scope='session')
def django_db_setup():
    """使用现有数据库测试"""
    pass
class BaseTestCase(TestCase):


    databases = '__all__'

    @classmethod
    def setUpClass(cls):
        import os
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
        super().setUpClass()

    def setUp(self):
        settings.DEBUG = True
        self.factory = RequestFactory()


    def tearDown(self):
        pass
