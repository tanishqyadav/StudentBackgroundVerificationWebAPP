from django.urls import path
from . import views

urlpatterns = [
    path('', views.login),
    path('logout/', views.logout),
    path('signup/', views.signup),

]