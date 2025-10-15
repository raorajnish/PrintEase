from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view

app_name = 'app'

urlpatterns = [
    path('', views.home, name="home" ),
    # path('about/', views.about, name="about"),
    # path('contact/', views.contact, name="contact"),
    path('user-dashboard/', views.user_dashboard, name="user-dashboard"),
    path('shop-dashboard/', views.shop_dashboard, name="shop-dashboard"),
    path('shop-details/', views.shop_details_view, name='shop-details-form'),
    path('shop-print/<int:shop_id>/', views.shop_print_view, name='shop-print'),
    path('shop-details-modal/<int:shop_id>/', views.shop_details_modal, name='shop-details-modal'),
    path('past-orders/', views.past_orders, name='past-orders'),
    path('order-details/<int:order_id>/', views.order_details, name='order-details'),
    path('cancel-order/<int:order_id>/', views.cancel_order, name='cancel-order'),
    path('shop-orders/', views.shop_orders, name='shop-orders'),
    path('update-order-status/<int:order_id>/', views.update_order_status, name='update-order-status'),
    path('analytics/', views.analytics, name='analytics'),

] +static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

