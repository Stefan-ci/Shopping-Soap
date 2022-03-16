from blog import views
from django.urls import path

app_name = 'blog'

urlpatterns = [
   	path('postes/', views.posts_list_view, name='posts'),
   	path('postes/<str:slug>/', views.post_detail_view, name='post-detail'),
]
