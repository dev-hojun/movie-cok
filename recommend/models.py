from django.db import models
from django.contrib.auth.models import User
from common.models import CustomUser
from movie.models import Movie

# Create your models here.
class Survey(models.Model):
	user = models.OneToOneField(CustomUser, related_name='survey', on_delete=models.CASCADE, db_column='user', verbose_name='설문자')
	genre = models.TextField(verbose_name='장르')
	playtime = models.IntegerField(verbose_name='상영시간')
	date = models.TextField(verbose_name='개봉시기')
	age = models.IntegerField(verbose_name='연령등급')
	score_npro = models.IntegerField(verbose_name='네티즌평점중요도')
	score_pro = models.IntegerField(verbose_name='전문가평점중요도')
	score_gender = models.IntegerField(verbose_name='같은성별평점중요도')
	score_age = models.IntegerField(verbose_name='같은연령평점중요도')
	production = models.DecimalField(max_digits=5, decimal_places=2,verbose_name='연출중요도')
	acting = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='연기중요도')
	story = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='스토리중요도')
	visual = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='영상미중요도')
	ost = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='ost중요도')
	reult_list = models.TextField(null=True, blank=True, verbose_name='결과리스트')

class Recommend(models.Model):
	survey = models.ForeignKey(Survey, related_name='recommend', on_delete=models.CASCADE, db_column='survey', verbose_name='설문조사')
	user = models.ForeignKey(CustomUser, related_name='recommend', on_delete=models.CASCADE, db_column='user', verbose_name='설문자')
	movie = models.ForeignKey(Movie, related_name='recommend', on_delete=models.CASCADE, db_column='movie', verbose_name='영화')
	similarity = models.DecimalField(max_digits=10, decimal_places=8, verbose_name='유사도')
	total = models.DecimalField(max_digits=10, decimal_places=8, verbose_name='총점')