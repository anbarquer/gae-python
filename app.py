#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import os
import jinja2
import urllib
import random

from config import VIEWS, URLS
from models import AppUser, Product, ndb

from google.appengine.api import users

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


def get_user_key(user):
    return str(AppUser.query(AppUser.identity == user.user_id()).get().key.id())


class MainHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        products = []
        if user:
            url_linktext = 'Logout'
            url = users.create_logout_url(self.request.uri)
            app_user = AppUser.get_or_insert(user.user_id(),
                                             identity=user.user_id(),
                                             email=user.email())
            keys = [ndb.Key(Product, int(k)) for k in app_user.products]
            if keys:
                products = ndb.get_multi(keys)
                products = filter(None, products)
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'
        template = JINJA_ENVIRONMENT.get_template(VIEWS['index'])
        self.response.write(
            template.render({'user': user, 'url': url, 'url_linktext': url_linktext, 'products': products}))


class ProductsHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        products = Product.query().order(Product.cost)
        app_user = None
        if user:
            app_user = AppUser.get_or_insert(get_user_key(user),
                                             identity=user.user_id(),
                                             email=user.email())
        template = JINJA_ENVIRONMENT.get_template(VIEWS['products'])
        self.response.write(template.render({'products': products, 'user': app_user}))

    def post(self):
        user = users.get_current_user()
        action = self.request.POST.get('action')
        if user:
            if action == 'create':
                product = Product(name='product ' + str(random.randint(1, 20)), cost=random.randint(1, 100))
                product.put()

            else:
                product = Product.get_by_id(int(self.request.POST.get('id')))
                app_user = AppUser.get_or_insert(get_user_key(user),
                                                 identity=user.user_id(),
                                                 email=user.email())
                if action == 'buy':
                    app_user.add_product(product)

                elif action == 'delete':
                    app_user.remove_product(product)
                    ndb.Key(Product, product.key.id()).delete()
        self.redirect(URLS['products'])


app = webapp2.WSGIApplication([
    (URLS['root'], MainHandler),
    (URLS['products'], ProductsHandler),

], debug=True)
