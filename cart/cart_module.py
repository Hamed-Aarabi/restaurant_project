from menu.models import Food
from django.shortcuts import get_object_or_404

CART_SESSION_ID = 'cart'  # key in session dict that named cart.


class Cart:
    def __init__(self, request):
        self.session = request.session  # create session
        cart = self.session.get(CART_SESSION_ID)
        if not cart:  # if in session dict any key named CART_SESSION_ID not found
            cart = self.session[CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        cart = self.cart.copy()

        for item in cart.values():
            item['food'] = get_object_or_404(Food, id=item['id'])
            item['total_price'] = int(item['quantity']) * int(item['price'])
            item['unique'] = self.unique_id_generator(item['id'], item['name'])
            yield item

    def unique_id_generator(self, id, name):
        result = f'{id}--{name}'
        return result

    def add(self, food, quantity):
        id_unique = self.unique_id_generator(food.id, food.name)
        if id_unique not in self.cart:
            self.cart[id_unique] = {'name': food.name, 'quantity': 0, 'price': str(food.price), 'id': str(food.id)}
        self.cart[id_unique]['quantity'] += int(quantity)
        self.save()

    def total(self):
        cart = self.cart
        total = sum(int(item['quantity']) * int(item['price']) for item in cart.values())
        return total

    def cart_len(self):
        return len(self.cart)

    def remove(self, id):
        cart = self.cart
        if id in cart:
            cart[id]['quantity'] -= 1
            if cart[id]['quantity'] == 0:
                del cart[id]
            self.save()


    def delete(self):
        del self.session[CART_SESSION_ID]

    def save(self):
        self.session.modified = True
