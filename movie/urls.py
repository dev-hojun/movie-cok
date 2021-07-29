from django.urls import path
from . import views

app_name = 'movie'

urlpatterns = [
	path('list/', views.list, name='list'),
	path('<int:movie_id>/', views.detail, name='detail'),
	path('comment/create/<int:movie_id>/', views.comment_create, name='comment_create'),
	path('comment/modify/<int:comment_id>/', views.comment_modify, name='comment_modify'),
	path('comment/delete/<int:comment_id>/', views.comment_delete, name='comment_delete'),
]