from django.urls import path
from . import views


urlpatterns = [
    path('inventory/', views.index, name='inventory'),
    path('inventory/collections/<str:slug>/', views.collectionView, name='collectionsView'),
    path('inventory/product/<str:pk>/', views.view_product, name='view_product'),
    path('inventory/add_product/', views.add_product, name='add_product'),
    path('inventory/add_category/', views.add_category, name='add_category'),
    path('inventory/product/update/<str:pk>/', views.update_product, name='update'),
    path('inventory/product/delete/<str:pk>/', views.delete_product, name='delete_product'),
]

