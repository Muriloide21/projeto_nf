from django.urls import path
from . import views

app_name = "fornecedores"
urlpatterns = [
    path('fornecedores/', views.list_fornecedores, name='list_fornecedores'),
    path('fornecedor/<int:id>/delete/', views.delete_fornecedor, name='delete_fornecedor'),
]