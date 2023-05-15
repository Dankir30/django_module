from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser


class MyUser(AbstractUser):
    wallet = models.DecimalField(max_digits=15, decimal_places=2, default=10_000)

    def decrease_wallet(self, product_price):
        self.wallet -= product_price
        self.save()

    def __str__(self):
        return self.username


class Product(models.Model):
    name = models.CharField(max_length=1000)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='static/images/', blank=True)
    balance = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    def decrease_balance(self, buy_amount):
        self.balance -= buy_amount
        self.save()

    def __str__(self):
        return self.name


class BuyItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    bought_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'buyItem {self.product} by {self.user}'


class BuyItemReturn(models.Model):
    buy_item = models.OneToOneField(BuyItem, on_delete=models.CASCADE)
    request_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'return {self.buy_item}'
