from google.appengine.ext import ndb


class AppUser(ndb.Model):
    identity = ndb.StringProperty(indexed=True)
    email = ndb.StringProperty(indexed=False)
    credits = ndb.FloatProperty(default=1000)
    products = ndb.StringProperty(repeated=True)

    def remove_product(self, product):
        try:
            ident = str(product.key.id())
            index = self.products.index(ident)
        except ValueError:
            index = -1
        else:
            self.products.remove(ident)
            self.credits += product.cost
            self.put()
        return index

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
