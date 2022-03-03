from django.urls import path
from collab_app import views

app_name = 'collab_app'
urlpatterns = [
    path('', views.index, name='index'),
]