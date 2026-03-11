from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog, name='blog'),
    path('categoria/<categoria_id>/', views.categoria, name='categorias'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
]
