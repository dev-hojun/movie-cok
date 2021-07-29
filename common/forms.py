from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
# from django.contrib.auth.models import User
# from django.contrib.auth import get_user_model
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
	email = forms.EmailField(label="이메일")

	class Meta:
		# model = get_user_model() 
		model = CustomUser 
		fields = UserCreationForm.Meta.fields + ('gender', 'age', 'email')
		# fields = ("username", "email")
		
class CustomUserChangeForm(UserChangeForm) :
	class Meta :
		# model = User
		# model = get_user_model() 
		model = CustomUser
		# 만약 User모델을 직접 참조하게 되면, 나중에 User를 Custom 했을 때의 User를 참조할 수 없게 됨. 그래서 간접적으로 참조하는 방식을 취하는 것이 좋음
		fields = ("username", 'gender', 'age', "email", "password")
		# fields = UserChangeForm.Meta.fields