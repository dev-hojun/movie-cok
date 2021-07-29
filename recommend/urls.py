from django.urls import path
from . import views

app_name = 'recommend'

urlpatterns = [
	# path('survey/list/', views.list, name='list'),
	path('survey/detail/', views.detail, name='detail'),
	path('survey/create/', views.survey_create, name='survey_create'),
	path('survey/modify/<int:survey_id>/', views.survey_modify, name='survey_modify'),
	path('survey/delete/<int:survey_id>/', views.survey_delete, name='survey_delete'),
	path('recommend', views.recommend, name='recommend'),
]