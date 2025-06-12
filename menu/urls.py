from django.urls import path
from . import views

urlpatterns = [
    path('', views.menu_list, name='menu_list'),
    path('create/', views.menu_create, name='menu_create'),
    path('update/<int:pk>/', views.menu_update, name='menu_update'),
    path('delete/<int:pk>/', views.menu_delete, name='menu_delete'),
    path('update-sold/<int:pk>/', views.update_sold_servings, name='update_sold_servings'),
    path('purchase/<int:pk>/', views.purchase_menu, name='purchase_menu'),
] 