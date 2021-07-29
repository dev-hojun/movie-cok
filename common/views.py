from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout, update_session_auth_hash
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
# from django.contrib.auth import get_user_model
# UserModel = get_user_model()
# Create your views here.
# from movie.models import Movie, Score

def index(request):
    # data = {}
    # select_code = 17972
    # data['movie'] = Movie.objects.get(code=select_code)
    # data['score'] = Score.objects.get(code=select_code)

    return render(request, 'common/base.html')

def login(request):
	if request.user.is_authenticated:
		return redirect('/common')
	else:
		if request.method == 'POST':
			form = AuthenticationForm(request, request.POST)

			if form.is_valid():
				auth_login(request, form.get_user())
				return redirect('/common')
		else:
			form = AuthenticationForm
		return render(request, 'common/login.html', {'form': form})
		
@login_required
def logout(request) :
    auth_logout(request)
    return redirect('/common')
	
def signup(request):
	if request.user.is_authenticated:
		return redirect('/common')
	else:
		if request.method == "POST":
			form = CustomUserCreationForm(request.POST)
			if form.is_valid():
				form.save()
				username = form.cleaned_data.get('username')
				raw_password = form.cleaned_data.get('password1')
				user = authenticate(username=username, password=raw_password)
				auth_login(request, user)
				# user = UserModel.objects.get(username=username)
				
				# if(user.is_superuser):
					# print("슈퍼유저")
				# else:
					# print("일반유저)
					
				return redirect('/common')
		else:
			form = CustomUserCreationForm()
		return render(request, 'common/signup.html', {'form': form})
		# return render(request, 'common2/signup2.html', {'form': form})

@login_required
def delete(request) :
	# if not request.user.is_authenticated:
		# return redirect('/common/login')
	# else:
		if request.method == "POST":
			request.user.delete()
			auth_logout(request) # 세션 지워주기
			return redirect('/common')
		else:
			return redirect('/common')

@login_required
def changeinfo(request) :
	if request.method == "POST" :
		form = CustomUserChangeForm(request.POST, instance=request.user)
		if form.is_valid() :
			form.save()
			return redirect('/common/mypage')
	else :
		form = CustomUserChangeForm(instance=request.user)
		# user_form = CustomUserChangeForm(instance=request.user)
		# password_form = PasswordChangeForm(request.user, request.POST)
	# context = {
		# user_form,
		# password_form
	# }
	return render(request, 'common/changeinfo.html', {'form': form})

@login_required
def changepw(request) :
	if request.method == "POST" :
		form =PasswordChangeForm(request.user, request.POST)
		if form.is_valid() :
			user = form.save() # 이때 로그아웃처리됨. session 정보 날라가고, 로그인정보도 사라짐
			update_session_auth_hash(request, user) # session 을 update 이렇게 해야 비밀번호를 바꾸더라도 로그아웃이 되지 않음
			return redirect('/common/mypage')
	else :
		form = PasswordChangeForm(request.user)
	return render(request, 'common/changepw.html', {'form': form})

@login_required
def mypage(request):
    return render(request, 'common/mypage.html')