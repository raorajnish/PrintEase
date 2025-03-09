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

] +static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

