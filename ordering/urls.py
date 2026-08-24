from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('add-funds/', views.add_dummy_funds, name='add_dummy_funds'),
    path('register/', views.register, name='register'),
]