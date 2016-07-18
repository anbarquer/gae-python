# DIRECTORIES
BASE_TEMPLATES = 'templates'

# TEMPLATES
INDEX = BASE_TEMPLATES + '/index.html'
LOGIN = BASE_TEMPLATES + '/login.html'
REGISTER = BASE_TEMPLATES + '/register.html'
DASHBOARD = BASE_TEMPLATES + '/dashboard.html'
PRODUCTS = BASE_TEMPLATES + '/products.html'

# URLS
ROOT_URL = '/'
INDEX_URL = '/index'
LOGIN_URL = '/login'
REGISTER_URL = '/register'
DASHBOARD_URL = '/dashboard'
PRODUCTS_URL = '/products'

# VIEWS
VIEWS = {'index': INDEX, 'login': LOGIN, 'register': REGISTER, 'dashboard': DASHBOARD, 'products': PRODUCTS}
URLS = {'root':ROOT_URL, 'index': INDEX_URL, 'login': LOGIN_URL, 'register': REGISTER_URL, 'dashboard': DASHBOARD_URL, 'products': PRODUCTS_URL}
