import datetime

from django.contrib import messages
from django.forms import ModelForm, forms
from shop_app.models import MyUser, Product, BuyItem, BuyItemReturn


class RegisterForm(ModelForm):
    class Meta:
        model = MyUser
        fields = ("username", "first_name", "last_name", "password")

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image', 'balance']

    def clean(self):
        cleaned_data = super().clean()
        price = float(cleaned_data.get('price'))
        if price <= 0:
            raise forms.ValidationError('Incorrect price')


class BuyItemForm(ModelForm):
    class Meta:
        model = BuyItem
        fields = ['amount']

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        if 'product_id' in kwargs:
            self.product_id = kwargs.pop('product_id')
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        try:
            product = Product.objects.get(pk=self.product_id)
            self.product = product
            if self.request.user.wallet < cleaned_data.get('amount') * product.price:
                self.add_error(None, "Error")
                messages.error(self.request, 'You don`t have enough money')
            if cleaned_data.get('amount') > product.balance:
                self.add_error(None, "Error")
                messages.error(self.request, 'Don`t have enough product')
        except Product.DoesNotExist:
            self.add_error(None, "Error")
            messages.error(self.request, 'Product doesn`t exist')


class BuyItemReturnForm(ModelForm):
    class Meta:
        model = BuyItemReturn
        fields = []

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(BuyItemReturnForm, self).__init__(*args, **kwargs)

    def clean(self):
        try:
            buy_item = BuyItem.objects.get(id=self.request.POST.get('new_return_id'))
            self.buy_item = buy_item
            bought_at = buy_item.bought_at.replace(tzinfo=datetime.timezone.utc)
            time_now = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
            time_delta = datetime.timedelta(minutes=3)
            time_edge = bought_at + time_delta
            if BuyItemReturn.objects.filter(buy_item=buy_item).exists():
                self.add_error(None, 'Error')
                messages.error(self.request, 'Purchase return is alredy exist.')
            if time_now > time_edge:
                self.add_error(None, "Error")
                messages.error(self.request, 'You can return purchase during 3 min, only')
        except BuyItem.DoesNotExist:
            self.add_error(None, "Error")
            messages.error(self.request, 'buy item doesn`t exist')