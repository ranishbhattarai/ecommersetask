from django.urls import path
from .views import (
    login_view, logout_view, register_view, product_list, product_detail, my_orders,
    admin_dashboard, supplier_dashboard, delivery_dashboard, dashboard, debug_session
)

urlpatterns = [
    path("", product_list),
    path("login/", login_view),
    path("register/", register_view),
    path("logout/", logout_view),
    path("products/<int:product_id>/", product_detail),
    path("orders/", my_orders),
    path("dashboard/", dashboard),
    path("dashboard/admin/", admin_dashboard),
    path("dashboard/supplier/", supplier_dashboard),
    path("dashboard/delivery/", delivery_dashboard),
    path("debug/session/", debug_session),
]