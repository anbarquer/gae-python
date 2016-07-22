#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import webapp2
import os
import jinja2
import random

from config import VIEWS, URLS, NAME_VALUES, PRICE_VALUES
from models import AppUser, Product, ndb

from google.appengine.api import users

# Variable de entorno para ejecutar Jinja2
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


def get_user_key(user):
    return str(AppUser.query(AppUser.identity == user.user_id()).get().key.id())


# Controlador para la página principal
class MainHandler(webapp2.RequestHandler):
    # Cada método HTTP tiene un método de clase, en este caso sólo se utiliza get()
    def get(self):
        user = users.get_current_user()
        products = []
        if user:
            url_linktext = 'Logout'
            # Función propia de la clase USER de App Engine
            url = users.create_logout_url(self.request.uri)
            # get_or_insert es una solución para obtener o crear un registro en caso de que
            # ya se encontrara guardado o no, respectivamente
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
        # A la función "render" se le pasa un diccionario de parámetros que se van a utilizar en la vista.
        # Estos parámetros vienen identificados por {{ }}
        self.response.write(
            template.render({'user': user, 'url': url, 'url_linktext': url_linktext, 'products': products}))


class ProductsHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        products = Product.query().order(Product.name)
        if user:
            app_user = AppUser.get_or_insert(get_user_key(user),
                                             identity=user.user_id(),
                                             email=user.email())
        else:
            return self.redirect(URLS['index'])
        template = JINJA_ENVIRONMENT.get_template(VIEWS['products'])
        self.response.write(template.render({'products': products, 'user': app_user}))

    def post(self):
        user = users.get_current_user()
        action = self.request.POST.get('action')
        # En la vista de productos, se envía un campo oculto llamado 'action'
        # Este campo puede tener tres valores distintos:
        # - 'create': se crea un nuevo producto aleatoriamente y se añade al listado principal de productos.
        # - 'buy': el usuario compra un nuevo producto.
        # - 'delete': se elimina un producto del listado principal.
        if action == 'create':
            product = Product(name='p' + str(random.randint(NAME_VALUES[0], NAME_VALUES[1])),
                              cost=random.randint(PRICE_VALUES[0], PRICE_VALUES[1]))
            product.put()
        elif user:
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

# Asociación de los controladores a las direcciones de la aplicación
app = webapp2.WSGIApplication([
    (URLS['index'], MainHandler),
    (URLS['products'], ProductsHandler),

], debug=True)  # Modo debug.
