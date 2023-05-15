"""
URL configuration for module_shop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
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
