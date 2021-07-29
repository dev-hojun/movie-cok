from django.shortcuts import render, redirect, get_object_or_404
from movie.models import Movie, Score, Comment
from .models import Survey, Recommend
from .forms import SurveyForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.utils import timezone
import datetime, calendar
from django.db.models import Q
import math, decimal

# Create your views here.
@login_required
def list(request):
	data = {}
	user =request.user
	
	surveylist = Survey.objects.filter(user=user)
	data['surveylist'] = surveylist
	
	return render(request, 'recommend/list.html', data)

@login_required
def detail(request):
	data = {}
	user =request.user

	if not Survey.objects.filter(user=user).exists():
		return redirect('recommend:survey_create')
	else:
		survey = Survey.objects.get(user=user)
		data['survey'] = survey

		return render(request, 'recommend/detail.html', data)

@login_required
def survey_create(request):
	data = {}

	if request.method == "POST":
		form = SurveyForm(request.POST)

		if form.is_valid():
			survey = form.save(commit=False)
			survey.user = request.user

			genres = request.POST.getlist('genre')
			survey.genre = ','.join(genres)
			start_date = request.POST.get('start_date')
			end_date = request.POST.get('end_date')
			survey.date = start_date + "," + end_date
			
			survey.save()
			return redirect('recommend:detail')
	else:
		if Survey.objects.filter(user=request.user).exists():
			return redirect('recommend:detail')
		form = SurveyForm()
	data['form'] = form

	return render(request, 'recommend/surveyform.html', data)

@login_required
def survey_modify(request, survey_id):
	pass

@login_required
def survey_delete(request, survey_id):
	survey = get_object_or_404(Survey, pk=survey_id)
	if request.user != survey.user:
		messages.error(request, '삭제권한이 없습니다')
		return redirect('recommend:list')
	else:
		survey.delete()
	return redirect('recommend:list')

@login_required
def recommend(request):
	data = {}
	user =request.user

	if not Survey.objects.filter(user=user).exists():
		return redirect('recommend:survey_create')
	else:
		survey = Survey.objects.get(user=user)
	
	if not Recommend.objects.filter(survey=survey).exists():	# 기존꺼 없을 경우 새로 생성
		# step1_list = Movie.objects.filter(Q(id=45477) | Q(id=61698) | Q(id=66751) | Q(id=22126) | Q(id=23525)) # 테스트용 영화 5개
		# step1_list = Movie.objects.filter(Q(id=45477) | Q(id=61698) | Q(id=66751)) # 테스트용 영화 3개
		step1_list = step1(request, survey)
		recommendlist = step2(request, survey, step1_list)
	else:	# 기존꺼 있을 경우 그대로 씀
		recommendlist = Recommend.objects.filter(survey=survey).order_by('-total')
		
	data['recommendlist'] = recommendlist
	data['survey'] = survey
	movielist = []
	for recommend in recommendlist:
		movielist.append(recommend.movie)
	data['movielist'] = movielist
	return render(request, 'recommend/recommend.html', data)

def step1(request, survey):
	# 장르로 선별
	genres = survey.genre.split(',')
	
	if len(genres) == 1:
		# print(genres[0])
		genrelist = Movie.objects.filter(Q(genre__contains=genres[0]))
	elif len(genres) == 2:
		# print(genres[0])
		# print(genres[1])
		genrelist = Movie.objects.filter(Q(genre__contains=genres[0]) | Q(genre__contains=genres[1]))
	elif len(genres) == 3:
		# print(genres[0])
		# print(genres[1])
		# print(genres[2])
		genrelist = Movie.objects.filter(Q(genre__contains=genres[0]) | Q(genre__contains=genres[1]) | Q(genre__contains=genres[2]))
	# print("장르로 선별 후 : " + str(len(genrelist)))
	# for genre in genrelist:
		# print(genre)
	# print("=================================")
	# 상영시간으로 선별
	playtime = survey.playtime
	# print(playtime)
	if(playtime == 200):
		playtimelist = genrelist
	else:
		playtimelist = genrelist.filter(Q(playtime__lte=playtime))
	# playtimelist = genrelist.filter(Q(playtime__lt=30)) # 테스트용
	# for playtime in playtimelist:
		# print(playtime)
	# print("상영시간으로 선별 후 : " + str(len(playtimelist)))
	# print("=================================")
	dates = survey.date.split(',')
	start = dates[0]
	end = dates[1]
	# print(start + " ~ " + end)
	datelist = playtimelist.filter(Q(date__gte=start) & Q(date__lt=end))
	# print("개봉시기로 거른 후 : " + str(len(datelist)))
	# for date in datelist:
		# print(date.date)
	# print("=================================")
	age = survey.age
	# print(age)
	agelist = datelist.filter(Q(age__lte=age))
	# print("연령등급으로 거른 후 : " + str(len(agelist)))
	
	return agelist
	
def step2(request, survey, step1_list):
	# total = decimal.Decimal(0)
	user = request.user
	top3_list = []
	
	for movie in step1_list:
		score = Score.objects.get(movie=movie)
		total = decimal.Decimal(0)
		# print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
		# print(str(movie) + "의 총점" + str(total))
		
		# 네티즌 평점, 전문가 평점 추가
		total += score.score_npro * survey.score_npro / 10 + score.score_pro * survey.score_pro / 10
		# print(str(movie) + "의 총점" + str(total))
		
		# 같은 성별 평점 추가
		if user.gender == 'M' :
			total += score.score_m * survey.score_gender / 10
		elif user.gender == 'W' :
			total += score.score_w * survey.score_gender / 10
		# print(str(movie) + "의 총점" + str(total))
		
		# 같은 연령 평점 추가
		if user.age == "10" :
			total += score.score_10 * survey.score_age / 10
		if user.age == "20" :
			total += score.score_20 * survey.score_age / 10
		if user.age == "30" :
			total += score.score_30 * survey.score_age / 10
		if user.age == "40" :
			total += score.score_40 * survey.score_age / 10
		if user.age == "50" :
			total += score.score_50 * survey.score_age / 10
		# print(str(movie) + "의 총점" + str(total))
		
		# 감상 포인트 추가
		similarity = ((score.production * survey.production + score.acting * survey.acting + score.story * survey.story + score.visual * survey.visual + score.ost * survey.ost) / decimal.Decimal(math.sqrt(math.pow(score.production, 2) + math.pow(score.acting, 2) + math.pow(score.story, 2) + math.pow(score.visual, 2) + math.pow(score.ost, 2)) * math.sqrt(math.pow(survey.production, 2) + math.pow(survey.acting, 2) + math.pow(survey.story, 2) + math.pow(survey.visual, 2) + math.pow(survey.ost, 2)))) * 40
		total += similarity
		# print(str(movie) + "의 총점" + str(total))
		# print("===============================================================")
		
		# Recommend 생성
		if len(top3_list) < 3:
			recommend = Recommend(survey=survey, user=user, movie=movie, similarity=similarity, total=total)
			top3_list.append(recommend)
			top3_list = bubbleSort(top3_list)
			# print("top3_list에 " + str(recommend.movie.title) + "추가")
		else:
			if top3_list[0].total < total:
				# print("top3_list에 " + str(top3_list[0].movie.title) + "제거")
				# print("top3_list에 " + str(movie.title) + "추가")
				top3_list.remove(top3_list[0])
				new_recommend = Recommend(survey=survey, user=user, movie=movie, similarity=similarity, total=total)
				top3_list.append(new_recommend)
				top3_list = bubbleSort(top3_list)
				# print("top3_list : " + str(top3_list[0].movie.title) + ", " + str(top3_list[1].movie.title) + ", " + str(top3_list[2].movie.title))
	# top3_list에 있는 Recommend 저장
	for recommend in top3_list:
		recommend.save()
	# total 점수로 정렬하여 리스트 생성
	step2_list = Recommend.objects.filter(survey=survey).order_by('-total')
	# for recommend in step2_list:
		# print(str(recommend.movie.id) + " 영화 총점 : " + str(recommend.total))
	return step2_list
	
def swap(list, i, j):
    list[i], list[j] = list[j], list[i]

def bubbleSort(list):
	for size in reversed(range(len(list))):
		for i in range(size):
			if list[i].total > list[i+1].total:
				swap(list, i, i+1)
	return list