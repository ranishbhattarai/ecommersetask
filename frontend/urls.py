from django.urls import path
from .views import login_view, logout_view, product_list, product_detail, my_orders

urlpatterns = [
    path("",product_list),
     path("login/",login_view),
    path("logout/",logout_view),
    path("products/<int:product_id>/",product_detail),
    path("orders/",my_orders),
   
]