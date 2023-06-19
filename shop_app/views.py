

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect

from django.shortcuts import redirect
from django.views.generic import DetailView, CreateView, ListView, UpdateView, DeleteView

from shop_app.forms import RegisterForm, ProductForm, BuyItemForm, BuyItemReturnForm
from shop_app.models import Product, BuyItemReturn, BuyItem
from django.db import transaction
from django.contrib import messages


class AdminPassedMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


class ProductListView(ListView):
    template_name = 'products.html'
    queryset = Product.objects.all()
    paginate_by = 9


class ProductDetailView(LoginRequiredMixin, DetailView):
    queryset = Product.objects.all()
    template_name = 'product_details.html'
    login_url = '/login/'
    extra_context = {'form': BuyItemForm()}


class MyLoginView(LoginView):
    template_name = 'login.html'


class MyLogout(LogoutView):
    next_page = '/'


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'register.html'
    success_url = '/'


class ProductCreateView(AdminPassedMixin, CreateView):
    form_class = ProductForm
    template_name = 'create_product.html'
    success_url = '/'


class ProductUpdateView(AdminPassedMixin, UpdateView):
    model = Product
    fields = ['name', 'description', 'price', 'image', 'balance']
    template_name = 'edit_product.html'
    success_url = '/'


class BuyItemListView(ListView):
    template_name = 'buy_items.html'
    queryset = BuyItem.objects.all()
    extra_context = {'form': BuyItemReturnForm()}

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)


class BuyItemCreateView(LoginRequiredMixin, CreateView):
    login_url = 'login/'
    model = BuyItem
    http_method_names = ['post']
    form_class = BuyItemForm
    success_url = '/'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({"request": self.request, "product_id": self.kwargs['pk']})
        return kwargs

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        product = form.product
        obj.product = product
        product.balance -= obj.amount
        self.request.user.wallet -= product.price * obj.amount
        with transaction.atomic():
            obj.save()
            product.save()
            self.request.user.save()
        messages.success(self.request, 'You bought ITEM')
        return super().form_valid(form=form)

    def form_invalid(self, form):
        return HttpResponseRedirect('/')


class BuyItemReturnCreateView(CreateView):
    http_method_names = ['post']
    success_url = '/'
    form_class = BuyItemReturnForm
    model = BuyItemReturn

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({"request": self.request})
        return kwargs

    def form_valid(self, form):
        obj = form.save(commit=False)
        buy_item = form.buy_item
        obj.buy_item = buy_item
        with transaction.atomic():
            obj.save()
        messages.success(self.request, f'You add return {obj.buy_item.product.name}')
        return super().form_valid(form=form)

    def form_invalid(self, form):
        return HttpResponseRedirect('/')


class BuyItemReturnListView(AdminPassedMixin, ListView):
    template_name = 'returns.html'
    queryset = BuyItemReturn.objects.all()


class ApproveReturnView(AdminPassedMixin, DeleteView):
    success_url = '/'
    model = BuyItem

    def form_valid(self, form):
        self.object.product.balance += self.object.amount
        self.object.user.wallet += self.object.amount * self.object.product.price

        with transaction.atomic():
            self.object.product.save()
            self.object.user.save()
        return super().form_valid(form=form)


class DeclineReturnView(AdminPassedMixin, DeleteView):
    success_url = '/'
    model = BuyItemReturn