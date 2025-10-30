from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('watch/<str:pk>/', views.watch, name='watch'),
    path('genre/<str:pk>/', views.genre, name='genre'),
    path('my-list', views.my_list, name='my-list'),
    path('add-to-list', views.add_to_list, name='add-to-list'),
    path('search', views.search, name='search'),
    path('api/movies/', views.movies_api, name='movies_api'),
    path('api/my-list/', views.my_list_api, name='my-list-api'),
]