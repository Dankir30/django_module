from django.contrib import admin
from django.urls import path
from shop_app.views import ProductListView, ProductDetailView, MyLoginView, RegisterView, MyLogout, ProductCreateView, \
    BuyItemListView, BuyItemCreateView, BuyItemReturnListView, ProductUpdateView, BuyItemReturnCreateView, \
    ApproveReturnView, DeclineReturnView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', ProductListView.as_view(), name='products'),
    path('product/<int:pk>', ProductDetailView.as_view(), name='details'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', MyLoginView.as_view(), name='login'),
    path('logout/', MyLogout.as_view(), name='logout'),
    path('create/', ProductCreateView.as_view(), name='create'),
    path('buy_items/', BuyItemListView.as_view(), name='buy_items'),
    path('new_buy_item/<int:pk>', BuyItemCreateView.as_view(), name='new_buy_item'),
    path('returns/', BuyItemReturnListView.as_view(), name='returns'),
    path('edit/product/<int:pk>', ProductUpdateView.as_view(), name='edit'),
    path('new_return/', BuyItemReturnCreateView.as_view(), name='new buyItem return'),
    path('delete_buy_item_return/<int:pk>', DeclineReturnView.as_view(), name='delete_return'),
    path('delete_buy_item/<int:pk>', ApproveReturnView.as_view(), name='delete_buy_item')
]