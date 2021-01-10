from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('payment/', views.payment, name='payment'),
    path('thanks/', views.thanks, name='thanks'),
    path('info/', views.info, name='info'),
    path('register/', views.register, name='register'),
]
