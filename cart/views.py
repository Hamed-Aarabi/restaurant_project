from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import View
from menu.models import Food
from .cart_module import Cart
from .models import Order, OrderItem, Discount


class CartDetailView(View):
    def get(self, request):
        cart = Cart(request)
        return render(request, 'cart/cart_detail.html', {'cart': cart})


class AddToCartView(View):
    def get(self, request):
        cart = Cart(request)
        client = request.session.get(f'{request.user.id}')
        if client:
            orders = client['orders'].values()
            for item in orders:
                food = get_object_or_404(Food, id=item['id'])
                quantity = item['quantity']
                cart.add(food, quantity)
            else:
                del client['orders']
                request.session.modified = True
        return redirect(reverse('cart:cart_detail'))


class RemoveItemCartView(View):
    def get(self, request, id):
        cart = Cart(request)
        cart.remove(id)
        return redirect('cart:cart_detail')


class CreateOrderView(View):
    def post(self, request):
        cart = Cart(request)
        if cart.cart_len() > 0:
            order = Order.objects.create(client=request.user, order_total_price=cart.total(),
                                         address=request.POST.get('address'))
            print(request.POST.get('address'))
            for item in cart:
                OrderItem.objects.create(order=order, food_name=item['name'], quantity=item['quantity'],
                                         price=item['price'], total_price=item['total_price'])
            cart.delete()
            return redirect('cart:order_detail', order.id)


class OrderDetailView(View):
    def get(self, request, id):
        order = get_object_or_404(Order, client_id=request.user.id, id=id)
        return render(request, 'cart/order_detail.html', {'order': order})

    def post(self, request, id):
        order = get_object_or_404(Order, client_id=request.user.id, id=id)
        discount_code = request.POST.get('discount-code')
        if Discount.objects.filter(code=discount_code, expired=False).exists():
            discount = Discount.objects.get(code=discount_code)
            order.order_total_price = int(order.order_total_price) * int(discount.percent) / 100
            order.save()
            discount.quantity -= 1
            if discount.quantity == 0:
                discount.expired = True
            discount.save()
            return redirect('cart:order_detail', order.id)

        else:
            messages.error(request, 'Invalid Code!!')
            return redirect('cart:order_detail', order.id)


class PaymentView(View):
    def get(self, request, id):
        order = get_object_or_404(Order, id=id, client_id=request.user.id)
        return render(request, 'cart/payment.html', {'order': order})

    def post(self, request, id):
        order = get_object_or_404(Order, id=id, client_id=request.user.id)
        if order:
            order.paid = True
            order.save()
            status = 'success'
            return render(request, 'cart/success_or_failed_pay.html', {'status': status})
        else:
            status = 'failed'
            return render(request, 'cart/success_or_failed_pay.html', {'status': status})
