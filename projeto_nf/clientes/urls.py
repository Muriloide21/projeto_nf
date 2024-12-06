from django.urls import path
from . import views

app_name = "clientes"
urlpatterns = [
    path('', views.list_clientes, name='list_clientes'),
    path('<int:id>/delete/', views.delete_cliente, name='delete_cliente'),
]