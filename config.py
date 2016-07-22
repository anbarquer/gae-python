#!/usr/local/bin/python
# -*- coding: utf-8 -*-

# DIRECTORIES
BASE_TEMPLATES = 'templates'

# TEMPLATES
INDEX = BASE_TEMPLATES + '/index.html'
PRODUCTS = BASE_TEMPLATES + '/products.html'

# URLS
INDEX_URL = '/'
PRODUCTS_URL = '/products'

# VIEWS
VIEWS = {'index': INDEX, 'products': PRODUCTS}
URLS = {'index': INDEX_URL, 'products': PRODUCTS_URL}

# PRODUCTS STATS
NAME_VALUES = [1, 20]
PRICE_VALUES = [1, 100]
