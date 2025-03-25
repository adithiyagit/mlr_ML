from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Make '' (empty) path point to home view
    path('list/', views.energy_consumption_list, name='energy_list'),
    path('predict/', views.predict_energy_consumption, name='predict_energy'),
]