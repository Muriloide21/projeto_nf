from django.urls import path
from . import views

app_name = "nota_fiscal"
urlpatterns = [
    path('', views.index, name='index'),
    path('nfs/', views.list_nfs, name='list_nfs'),
    path('nf/<int:id>/', views.detail_nf, name='detail_nf'),
    path('nf/<int:id>/delete/', views.delete_nf, name='delete_nf'),
]