from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from menu.models import Food


class FoodMenuView(ListView):
    template_name = 'menu/food_menu.html'
    model = Food
    context_object_name = 'foods'



class FoodDetailView(LoginRequiredMixin,DetailView):
    template_name = 'menu/food_detail.html'
    context_object_name = 'food'
    model = Food

    def post(self, request, pk):
        food = get_object_or_404(Food, id=pk)
        quantity = request.POST.get('quantity')
        total_price = int(food.price) * int(quantity)

        if not request.session.get(f'{request.user.id}'):
            request.session[f'{request.user.id}'] = {}
        client = request.session.get(f'{request.user.id}')
        if not client.get('orders'):
            client['orders'] = {}
        orders = client.get('orders')
        if not orders.get(f'{food.name}'):
            orders[f'{food.name}'] = {'name': food.name, 'quantity': 0, 'price': food.price, 'total_price': 0,
                                      'id': str(food.id)}
        orders[f'{food.name}']['quantity'] += int(quantity)
        orders[f'{food.name}']['total_price'] += int(total_price)
        request.session.modified = True
        # del request.session[f'{request.user.id}']
        # request.session.modified = True
        return redirect('menu:menu')


class ManageOrdersView(View):
    def get(self, request):
        if request.user.is_authenticated:
            client = request.session.get(str(request.user.id))
            if client:
                orders = client['orders'].values()
                return render(request, 'menu/manage_orders.html', {'orders': orders})
            else:
                return render(request, 'menu/manage_orders.html')
        else:
            return render(request, 'menu/manage_orders.html')


class DeleteOrderView(LoginRequiredMixin,View):
    def get(self, request, pk):
        client = request.session[f'{request.user.id}']
        food = get_object_or_404(Food, id=pk)
        del client['orders'][food.name]
        request.session.modified = True
        return redirect('menu:manage-orders')
