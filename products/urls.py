print("Loading products/urls.py")

from django.contrib import admin
from django.urls import path, include
from .import views

print("Views imported in products/urls.py")
print(dir(views))

urlpatterns = [
    path('', views.all_products, name='products'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),

]

print("URLs defined in products/urls.py")