from statistics import mean
from django.views.generic.edit import FormView
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.db.models import CharField
from django.db.models.functions import Length
from django.db.models import F

from .forms import OrderForm
from .models import Order


class LoginFormView(FormView):
    """Login Form"""
    form_class = AuthenticationForm
    template_name = "login.html"
    success_url = "/menu"

    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)


@login_required(login_url='/')
def menu_view(request):
    """View for menu page"""
    return render(request, 'menu.html', {})


@login_required(login_url='/')
def order_new(request):
    """View for new order"""
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=True)
            order.user = str(request.user)
            order.save()
            return redirect('statistics')
    else:
        form = OrderForm()
    return render(request, 'cart.html', {'form': form})


@login_required(login_url='/')
def statistics_view(request):
    """View for statistics page """
    user = str(request.user)  # get name of an authorized user for queries to DB
    data = Order.objects
    data_dict = {}
    data_dict['users_products'] = data.filter(user=user).count()
    data_dict['all_products'] = data.all().count()
    data_dict['users_max_price'] = max([query.price for query in data.filter(user=user)])
    data_dict['avg_all_price'] = round(mean([query.price for query in data.all()]))
    CharField.register_lookup(Length)  # register lookup
    data_dict['sum_users_price'] = sum([query.price for query in data.filter(user=user)])
    data_dict['complex_query'] = sum([data.filter(price__gt=50).count(),
                                      data.filter(user=user).filter(name__length__gt=3).count()])
    if request.method == "POST":
        Order.objects.all().update(price=F('price') + 1)
        return redirect('statistics')
    return render(request, 'statistics.html', {'data': data_dict})
