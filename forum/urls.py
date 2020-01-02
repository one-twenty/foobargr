from django.urls import path, include
from . import views


app_name = 'forum'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('register/', views.register_request, name='register'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('create-topic', views.create_topic, name='create-topic'),
    path('category/<slug:category>/', views.category_request, name='category'),
    path('topic/<int:topicID>/', views.topic_request, name='topic'),
]
