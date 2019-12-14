from django.urls import path, include
from . import views


app_name = 'forum'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('register/', views.register, name='register'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('category/<slug:category>/', views.category_request, name='category'),
    path('create-topic', views.create_topic, name='create-topic')
]
