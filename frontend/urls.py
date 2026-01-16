from django.urls import path
from .views import (
    login_view, logout_view, register_view, product_list, product_detail, my_orders,
    admin_dashboard, supplier_dashboard, delivery_dashboard, dashboard, debug_session, place_order,
    update_delivery_status, assign_delivery
)

urlpatterns = [
    path("", product_list, name='home'),
    path("products/", product_list, name='products'),
    path("login/", login_view),
    path("register/", register_view),
    path("logout/", logout_view),
    path("products/<int:product_id>/", product_detail),
    path("products/<int:product_id>/order/", place_order, name='place_order'),
    path("orders/", my_orders),
    path("dashboard/", dashboard),
    path("dashboard/admin/", admin_dashboard),
    path("dashboard/admin/assign/<int:order_id>/", assign_delivery, name='assign_delivery'),
    path("dashboard/supplier/", supplier_dashboard),
    path("dashboard/delivery/", delivery_dashboard),
    path("dashboard/delivery/<int:delivery_id>/update/", update_delivery_status, name='update_delivery_status'),
    path("debug/session/", debug_session),
]