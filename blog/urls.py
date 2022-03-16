from blog import views
from django.urls import path

app_name = 'blog'

urlpatterns = [
   	path('', views.posts_list_view, name='posts'),
   	path('<str:slug>/', views.post_detail_view, name='post-detail'),
]
