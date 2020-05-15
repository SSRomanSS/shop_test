from django.views.generic.edit import FormView
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .forms import OrderForm


class LoginFormView(FormView):
    form_class = AuthenticationForm
    template_name = "login.html"
    success_url = "/menu"

    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)

@login_required(login_url='/')
def menu_view(request):
    return render(request, 'menu.html', {})

@login_required(login_url='/')
def order_new(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            #order.save()
            return redirect('menu')
    else:
        form = OrderForm()
    return render(request, 'cart.html', {'form': form})
