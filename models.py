#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from google.appengine.ext import ndb


class AppUser(ndb.Model):
    identity = ndb.StringProperty(indexed=True)
    email = ndb.StringProperty(indexed=False)
    credits = ndb.FloatProperty(default=1000)
    products = ndb.StringProperty(repeated=True)

    def remove_product(self, product):
        # Como el usuario puede comprar varias veces el mismo producto, en caso de eliminarlo del sistema también se elimina del usuario
        # identificado actual por lo que es necesario
        self.credits += self.products.count(str(product.key.id())) * product.cost
        self.products = [p for p in self.products if p != str(product.key.id())]
        self.put()

    def add_product(self, product):
        success = True
        if self.credits >= product.cost:
            self.products.append(str(product.key.id()))
            self.credits -= product.cost
            self.put()
        else:
            success = False
        return success


class Product(ndb.Model):
    name = ndb.StringProperty(indexed=True)
    cost = ndb.FloatProperty(default=0)
