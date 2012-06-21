#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file demonstrates writing tests using the unittest module. These will pass
when you run \"manage.py test\".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

from models import *
from util import *
from django.contrib.auth.models import User


class TestDatasetModel(TestCase):

    fixtures = ['tests_data.json']

    def setUp(self):
        self.d1 = Dataset.objects.get(name='d1')
        self.d2 = Dataset.objects.get(name='d2')
        self.dd1 = Datum.objects.get(name='dd1.png')
        self.dd2 = Datum.objects.get(name='dd2.png')
        self.a1 = DatumAttachment.objects.get(name='a1')
        self.a2 = DatumAttachment.objects.get(name='a2')
        self.u1 = User.objects.get(username='u1')
        self.u2 = User.objects.get(username='u2')
        self.imgdt = DataType.objects.get(name='image')

    def test_dataset_is_user_allowed(self):
        self.assertTrue(self.d1.is_user_allowed(self.u1))
        self.assertTrue(self.d1.is_user_allowed(self.u2))
        self.assertTrue(self.dd1.is_user_allowed(self.u1))
        self.assertTrue(self.dd1.is_user_allowed(self.u2))
        self.assertTrue(self.a1.is_user_allowed(self.u1))
        self.assertTrue(self.a1.is_user_allowed(self.u2))

        self.assertTrue(self.d2.is_user_allowed(self.u2))
        self.assertTrue(self.dd2.is_user_allowed(self.u2))
        self.assertTrue(self.a2.is_user_allowed(self.u2))

    def test_user_not_allowed(self):
        self.assertFalse(self.d2.is_user_allowed(self.u1))
        self.assertFalse(self.dd2.is_user_allowed(self.u1))
        self.assertFalse(self.a2.is_user_allowed(self.u1))

    def test_datasetcolaborators(self):
        self.assertEquals(self.d1.colaborators().count(), 2)
        self.assertEquals(self.d2.colaborators().count(), 1)

    def test_typeaccept(self):
        self.assertTrue(self.imgdt.is_acceptable('test.png'))
        self.assertFalse(self.imgdt.is_acceptable('test.avi'))


class TestUtils(TestCase):

    def test_basename(self):
        self.assertEquals(base_name('asdf.tar.gz'), 'asdf')
        self.assertEquals(base_name('/root/ver_strange.dir/asdf.tar.gz'), 'asdf')
        self.assertEquals(base_name(r'c:\Windows With Spaces\asdf.tar.gz'), 'asdf')

    def test_extension_name(self):
        self.assertEquals( extension_name('/root/very_strang&@.dir/asdf.tar.gz'), 'tar.gz')
        self.assertEquals(extension_name(r'c:\Windows With Spaces\sdf.tar.gz'), 'tar.gz')
        self.assertEquals(extension_name('asdf.tar.gz'), 'tar.gz')
        self.assertEquals(extension_name('asdf'), '')


