class Cart:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        cart = self.session.get('cart')

        if not cart:
            cart = self.session['cart'] = {}
        else:
            self.cart = cart

    def add(self, product):
        if str(product.id) not in self.cart.keys():
            self.cart[product.id] = {
                'id': product.id,
                'title': product.title,
                'price': product.price,
                'quantity': 1,
                'image': product.image.url
            }
        else:
            for key, value in self.cart.items():
                if key == str(product.id):
                    value['quantity'] = value['quantity'] + 1
                    break
        self.save()

    def decrement(self, product):
        for key, value in self.cart.items():
            if key == str(product.id):
                value['quantity'] = value['quantity'] - 1
                if value['quantity'] < 1:
                    self.remove(product)
                else:
                    self.save()
                break
        else:
            print('There is no product with this id in your cart')

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def save(self):
        self.session['cart'] = self.cart
        self.session.modified = True

    def clear(self):
        self.session['cart'] = {}
        self.session.modified = True