#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import unittest

print 'Setting up global environment'
# Configuración de los directorios
# Es necesario cambiar GAE_PATH para ejecutar las pruebas
GAE_PATH = os.environ['HOME'] + '/bin'
APP_ENGINE_PATH = GAE_PATH + '/google_appengine'
APP_ENGINE_LIB_PATH = APP_ENGINE_PATH + '/lib/yaml/lib'

sys.path.insert(1, APP_ENGINE_PATH)
sys.path.insert(1, APP_ENGINE_LIB_PATH)

print 'Done'

from google.appengine.api import memcache
from google.appengine.ext import ndb
from google.appengine.ext import testbed
from google.appengine.api import users
from models import AppUser, Product


def get_entity_memcache(entity_key):
    entity = memcache.get(entity_key)
    if entity is not None:
        return entity
    key = ndb.Key(urlsafe=entity_key)
    entity = key.get()
    if entity is not None:
        memcache.set(entity_key, entity)
    return entity


class ProductTest(unittest.TestCase):
    def setUp(self):
        print '\nSetting up test environment for: ' + self.__str__().split(' ', 1)[0]
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        ndb.get_context().clear_cache()

    def tearDown(self):
        print 'Tearing down test environment for: ' + self.__str__().split(' ', 1)[0]
        self.testbed.deactivate()

    def testProducts(self):
        print ' --- Products tests -- '
        product1 = Product(name='product1', cost=1)
        product2 = Product(name='product2', cost=2)
        product3 = Product(name='product3', cost=3)

        assert product1.cost == 1
        assert product2.cost == 2
        assert product3.cost == 3

        assert product1.name == 'product1'
        assert product2.name == 'product2'
        assert product3.name == 'product3'

        product1_key = product1.put().urlsafe()
        product2_key = product2.put().urlsafe()
        product3_key = product3.put().urlsafe()

        retrieved_product1 = get_entity_memcache(product1_key)
        retrieved_product2 = get_entity_memcache(product2_key)
        retrieved_product3 = get_entity_memcache(product3_key)

        assert retrieved_product1 is not None
        assert retrieved_product2 is not None
        assert retrieved_product3 is not None

        assert retrieved_product1.name == product1.name
        assert retrieved_product2.name == product2.name
        assert retrieved_product3.name == product3.name

        assert retrieved_product1.cost == product1.cost
        assert retrieved_product2.cost == product2.cost
        assert retrieved_product3.cost == product3.cost


class AppUserTest(unittest.TestCase):
    def setUp(self):
        print '\nSetting up test environment for: ' + self.__str__().split(' ', 1)[0]
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        ndb.get_context().clear_cache()

    def tearDown(self):
        print 'Tearing down test environment for: ' + self.__str__().split(' ', 1)[0]
        self.testbed.deactivate()

    def testAppUser(self, ident='123', email='test@example.com', is_admin='0'):
        print ' --- App users tests --- '
        assert not users.get_current_user()

        self.testbed.setup_env(
            USER_EMAIL=email,
            USER_ID=ident,
            USER_IS_ADMIN=is_admin,
            overwrite=True)

        user = users.get_current_user()

        assert user.email() == email
        assert user.user_id() == ident

        app_user = AppUser(identity=user.user_id(), email=user.email())
        assert app_user.identity == user.user_id()
        assert app_user.email == user.email()

        app_user_key = app_user.put().urlsafe()

        retrieved_app_user = get_entity_memcache(app_user_key)
        assert retrieved_app_user is not None
        assert retrieved_app_user.identity == user.user_id()
        assert retrieved_app_user.email == user.email()

        product1 = Product(name='product1', cost=1)
        product2 = Product(name='product2', cost=2)
        product3 = Product(name='product3', cost=3)
        product1_key = product1.put().urlsafe()
        product2_key = product2.put().urlsafe()
        product3_key = product3.put().urlsafe()

        retrieved_product1 = get_entity_memcache(product1_key)
        retrieved_product2 = get_entity_memcache(product2_key)
        retrieved_product3 = get_entity_memcache(product3_key)

        app_user.add_product(retrieved_product1)
        app_user.add_product(retrieved_product2)
        app_user.add_product(retrieved_product3)

        assert len(app_user.products) > 0
        assert len(app_user.products) == 3

        app_user.remove_product(retrieved_product1)
        assert len(app_user.products) > 0
        assert len(app_user.products) == 2

        app_user.remove_product(retrieved_product2)
        app_user.remove_product(retrieved_product3)

        assert len(app_user.products) == 0


if __name__ == '__main__':
    unittest.main()
