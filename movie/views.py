from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Score, Comment
from .forms import CommentForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.utils import timezone
import datetime, calendar
from django.core.paginator import Paginator
from django.db.models import Q

# Create your views here.
def list(request):
   data = {}
   
   page = request.GET.get('page', '1')
   kw = request.GET.get('kw', '')
   print("page : " + page + ", kw : " + kw)
   # movielist = Movie.objects.all()
   # data['movielist'] = movielist
   movielist = Movie.objects.order_by('-date')
   if kw:
      movielist = movielist.filter(Q(title__contains=kw)).distinct()
      
   paginator = Paginator(movielist, 12)
   page_obj = paginator.get_page(page)
   data['movielist'] = page_obj
   data['page'] = page
   data['kw'] = kw
   
   return render(request, 'movie/list.html', data)
   
def detail(request, movie_id):
   data = {}

   # data['movie'] = Movie.objects.get(id=movie_id)
   data['movie'] = get_object_or_404(Movie, pk=movie_id)
   
   return render(request, 'movie/detail.html', data)
   
@login_required
def comment_create(request, movie_id):
   data = {}
   movie = get_object_or_404(Movie, pk=movie_id)
   if request.method == "POST":
      # point = {}
      form = CommentForm(request.POST)
      if form.is_valid():
         comment = form.save(commit=False)
         # comment.point = request.POST.getlist('point')
         comment.author = request.user
         comment.create_date = timezone.now()
         comment.movie = movie
         comment.save()
         update_score(comment.movie, comment.author, comment)
         return redirect('movie:detail', movie_id=movie.id)
   else:
      form = CommentForm()
   data['form'] = form
   data['movie'] = movie

   return render(request, 'movie/commentform.html', data)
   
@login_required
def comment_modify(request, comment_id):
    data = {}
    comment = get_object_or_404(Comment, pk=comment_id)
    movie = comment.movie
    if request.user != comment.author:
        messages.error(request, '댓글수정권한이 없습니다')
        return redirect('movie:detail', movie_id=comment.movie.id)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.modify_date = timezone.now()
            comment.save()
            update_score(comment.movie, comment.author, comment)
            return redirect('movie:detail', movie_id=comment.movie.id)
    else:
        form = CommentForm(instance=comment)
    data['form'] = form
    data['movie'] = movie
    return render(request, 'movie/commentform.html', data)
   
@login_required
def comment_delete(request, comment_id):
   comment = get_object_or_404(Comment, pk=comment_id)
   if request.user != comment.author:
      messages.error(request, '댓글삭제권한이 없습니다')
      return redirect('movie:detail', movie_id=comment.movie.id)
   else:
      comment.delete()
   return redirect('movie:detail', movie_id=comment.movie.id)

def update_score(movie, user, comment):
   NAVERMOVIE = 100
   COUNT_GENDER = 0
   for comment in movie.comment.all():
      if comment.author.gender == user.gender:
         COUNT_GENDER += 1
   COUNT_AGE = 0
   for comment in movie.comment.all():
      if comment.author.age == user.age:
         COUNT_AGE += 1

   print("USER : " + user.username + ", SCORE : " + str(comment.score_user) + ", COUNT_GENDER : " + str(COUNT_GENDER) + ", COUNT_AGE : " + str(COUNT_AGE))
   print(user)
   # 네티즌 평점 반영
   score = movie.score
   print("바꿔야 될 점수 : " + str(score.score_npro))
   score_user = comment.score_user
   print(type(score_user))
   print("추가 될 점수 : " + str(score_user))
   count = movie.comment.count()
   print(count)
   print("평가에 참여한 사람 수 : " + str(count + 100))
   result = (movie.score.score_npro * (NAVERMOVIE + movie.comment.count() - 1) + comment.score_user) / (NAVERMOVIE + movie.comment.count())
   print(type(movie.score.score_npro))
   print(type(NAVERMOVIE + movie.comment.count() - 1))
   print(result)
   print(round(result,2))
   movie.score.score_npro = round(result,2)
   print("===============================================")
   # 성별 평점 반영
   if(user.gender == 'M'):
      print("남자")
      result_m = round((movie.score.score_m * int(NAVERMOVIE / 2 + COUNT_GENDER - 1) + comment.score_user) / int(NAVERMOVIE / 2 + COUNT_GENDER), 2)
      print("남자 평점 반영 후 : " + str(result_m))
      movie.score.score_m = result_m
      
      # print(movie.comment.count())
      # commentlist = movie.comment.filter(point='production')
      # print(commentlist.count())
      # print(comment.content)
      # print(str(comment.author.gender))
      # print(str(comment.author.filter(gender='M').count()))
      # number = commentlist.filter(author.gender='M').count()
      # print(number)
   elif(user.gender == 'W'):
      print("여자")
      result_w = round((movie.score.score_w * int(NAVERMOVIE / 2 + COUNT_GENDER - 1) + comment.score_user) / int(NAVERMOVIE / 2 + COUNT_GENDER), 2)
      print("여자 평점 반영 후 : " + str(result_w))
      movie.score.score_w = result_w
   print("===============================================")
   # 연령대별 평점 반영
   if user.age == '10':
      print("movie.score.score_10 : " + str(movie.score.score_10))
      print("int(NAVERMOVIE / 5 + COUNT_AGE - 1) : " + str(NAVERMOVIE / 5 + COUNT_AGE - 1))
      print("comment.score_user : " + str(comment.score_user))
      print("int(NAVERMOVIE / 5 + COUNT_AGE): " + str(int(NAVERMOVIE / 5 + COUNT_AGE)))
      print("movie.score.score_10 * int(NAVERMOVIE / 5 + COUNT_AGE - 1) + comment.score_user) / int(NAVERMOVIE / 5 + COUNT_AGE : " + str((movie.score.score_10 * int(NAVERMOVIE / 5 + COUNT_AGE - 1) + comment.score_user) / int(NAVERMOVIE / 5 + COUNT_AGE)))
      result_10 = round((movie.score.score_10 * int(NAVERMOVIE / 5 + COUNT_AGE - 1) + comment.score_user) / int(NAVERMOVIE / 5 + COUNT_AGE), 2)
      print("10대 평점 반영 후 : " + str(result_10))
      movie.score.score_10 = result_10
   elif user.age == '20':
      result_20 = round((movie.score.score_20 * int(NAVERMOVIE / 5 + COUNT_AGE - 1) + comment.score_user) / int(NAVERMOVIE / 5 + COUNT_AGE), 2)
      print("20대 평점 반영 후 : " + str(result_20))
      movie.score.score_20 = result_20
   elif user.age == '30':
      result_30 = round((movie.score.score_30 * int(NAVERMOVIE / 5 + COUNT_AGE - 1) + comment.score_user) / int(NAVERMOVIE / 5 + COUNT_AGE), 2)
      print("30대 평점 반영 후 : " + str(result_30))
      movie.score.score_30 = result_30
   elif user.age == '40':
      result_40 = round((movie.score.score_40 * int(NAVERMOVIE / 5 + COUNT_AGE - 1) + comment.score_user) / int(NAVERMOVIE / 5 + COUNT_AGE), 2)
      print("40대 평점 반영 후 : " + str(result_40))
      movie.score.score_40 = result_40
   elif user.age == '50':
      result_50 = round((movie.score.score_50 * int(NAVERMOVIE / 5 + COUNT_AGE - 1) + comment.score_user) / int(NAVERMOVIE / 5 + COUNT_AGE), 2)
      print("50대 평점 반영 후 : " + str(result_50))
      movie.score.score_50 = result_50
      
   print("===============================================")
   # 감상포인트 반영
   if comment.point == 'production':
      print("production 수정 전 : " + str(movie.score.production))
      result1 = (movie.score.production / 100 * (NAVERMOVIE + movie.comment.count() - 1) + 1) / (NAVERMOVIE + movie.comment.count()) * 100
      print("production 수정 후 : " + str(result1))
      movie.score.production = round(result1, 2)
      movie.score.acting = round(movie.score.acting / 100 * (NAVERMOVIE + movie.comment.count() - 1) / (NAVERMOVIE + movie.comment.count()) * 100, 2)
      movie.score.story = round(movie.score.story / 100 * (NAVERMOVIE + movie.comment.count() - 1) / (NAVERMOVIE + movie.comment.count()) * 100, 2)
      movie.score.visual = round(movie.score.visual / 100 * (NAVERMOVIE + movie.comment.count() - 1) / (NAVERMOVIE + movie.comment.count()) * 100, 2)
      movie.score.ost = round(movie.score.ost / 100 * (NAVERMOVIE + movie.comment.count() - 1) / (NAVERMOVIE + movie.comment.count()) * 100, 2)
   elif comment.point == 'acting':
      print("acting 수정 전 : " + str(movie.score.acting))
      result2 = (movie.score.acting / 100 * (NAVERMOVIE + movie.comment.count() - 1) + 1) / (NAVERMOVIE + movie.comment.count()) * 100
      print("acting 수정 후 : " + str(result2))
      movie.score.acting = round(result2, 2)
      movie.score.production = round(movie.score.production / 100 * (NAVERMOVIE + movie.comment.count() - 1) / (NAVERMOVIE + movie.comment.count()) * 100, 2)
      movie.score.story = round(movie.score.story / 100 * (NAVERMOVIE + movie.comment.count() - 1) / (NAVERMOVIE + movie.comment.count()) * 100, 2)
      movie.score.visual = round(movie.score.visual / 100 * (NAVERMOVIE + movie.comment.count() - 1) / (NAVERMOVIE + movie.comment.count()) * 100, 2)
      movie.score.ost = round(movie.score.ost / 100 * (NAVERMOVIE + movie.comment.count() - 1) / (NAVERMOVIE + movie.comment.count()) * 100, 2)
   elif comment.point == 'story':
      print("story 수정 전 : " + str(movie.score.story))
      result3 = (movie.score.story / 100 * (NAVERMOVIE + movie.comment.count() - 1) + 1) / (NAVERMOVIE + movie.comment.count()) * 100
      print("story 수정 후 : " + str(result3))
      movie.score.story = round(result3, 2)
      movie.score.production = round(movie.score.production / 100 * (NAVERMOVIE + movie.comment.count() - 1) / (NAVERMOVIE + movie.comment.count()) * 100, 2)
      movie.score.acting = round(movie.score.acting / 100 * (NAVERMOVIE + movie.comment.count() - 1) / (NAVERMOVIE + movie.comment.count()) * 100, 2)
      movie.score.visual = round(movie.score.visual / 100 * (NAVERMOVIE + movie.comment.count() - 1) / (NAVERMOVIE + movie.comment.count()) * 100, 2)
      movie.score.ost = round(movie.score.ost / 100 * (NAVERMOVIE + movie.comment.count() - 1) / (NAVERMOVIE + movie.comment.count()) * 100, 2)
   elif comment.point == 'visual':
      print("visual 수정 전 : " + str(movie.score.visual))
      result4 = (movie.score.visual / 100 * (NAVERMOVIE + movie.comment.count() - 1) + 1) / (NAVERMOVIE + movie.comment.count()) * 100
      print("visual 수정 후 : " + str(result4))
      movie.score.visual = round(result4, 2)
      movie.score.production = round(movie.score.production / 100 * (NAVERMOVIE + movie.comment.count() - 1) / (NAVERMOVIE + movie.comment.count()) * 100, 2)
      movie.score.story = round(movie.score.story / 100 * (NAVERMOVIE + movie.comment.count() - 1) / (NAVERMOVIE + movie.comment.count()) * 100, 2)
      movie.score.acting = round(movie.score.acting / 100 * (NAVERMOVIE + movie.comment.count() - 1) / (NAVERMOVIE + movie.comment.count()) * 100, 2)
      movie.score.ost = round(movie.score.ost / 100 * (NAVERMOVIE + movie.comment.count() - 1) / (NAVERMOVIE + movie.comment.count()) * 100, 2)
   elif comment.point == 'ost':
      print("ost 수정 전 : " + str(movie.score.ost))
      result5 = (movie.score.ost / 100 * (NAVERMOVIE + movie.comment.count() - 1) + 1) / (NAVERMOVIE + movie.comment.count()) * 100
      print("ost 수정 후 : " + str(result5))
      movie.score.ost = round(result5, 2)
      movie.score.production = round(movie.score.production / 100 * (NAVERMOVIE + movie.comment.count() - 1) / (NAVERMOVIE + movie.comment.count()) * 100, 2)
      movie.score.story = round(movie.score.story / 100 * (NAVERMOVIE + movie.comment.count() - 1) / (NAVERMOVIE + movie.comment.count()) * 100, 2)
      movie.score.visual = round(movie.score.visual / 100 * (NAVERMOVIE + movie.comment.count() - 1) / (NAVERMOVIE + movie.comment.count()) * 100, 2)
      movie.score.acting = round(movie.score.acting / 100 * (NAVERMOVIE + movie.comment.count() - 1) / (NAVERMOVIE + movie.comment.count()) * 100, 2)
   print("이제 저장")
   print(str(movie.score.production) + " / " + str(movie.score.acting) + " / " + str(movie.score.story) + " / " + str(movie.score.visual) + " / " + str(movie.score.ost))
   movie.score.save()