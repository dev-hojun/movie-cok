from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'common'

urlpatterns = [
    path('', views.index, name='index'),   
	path('login/', views.login, name="login"),
    # path('login/', auth_views.LoginView.as_view(template_name='common/login.html'), name='login'),
	path('logout/', views.logout, name='logout'),
	# path('logout/', auth_views.LogoutView.as_view(), name='logout'),
	path('signup/', views.signup, name='signup'),
	path('delete/', views.delete, name='delete'),
	path('changeinfo/', views.changeinfo, name='changeinfo'),
	path('changepw/', views.changepw, name='changepw'),
	path('mypage/', views.mypage, name='mypage'),
]