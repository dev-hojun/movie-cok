from django.db import models
from django.contrib.auth.models import User
from common.models import CustomUser

# Create your models here.
class Movie(models.Model):
	id = models.IntegerField(primary_key=True, verbose_name='아이디')
	title = models.TextField(verbose_name='제목')
	genre = models.TextField(verbose_name='장르')
	nation = models.TextField(verbose_name='국가')
	playtime = models.IntegerField(verbose_name='상영시간')
	directors = models.TextField(verbose_name='감독')
	actors = models.TextField(verbose_name='배우')
	age = models.IntegerField(verbose_name='연령등급')
	date = models.DateField(verbose_name='개봉일')
	summary = models.TextField(null=True, blank=True, verbose_name='줄거리')
	image = models.URLField(verbose_name='이미지')
	
	def __str__(self):
		return str(self.id)
		
class Score(models.Model):
	# code = models.ForeignKey('Movie', related_name='movie', on_delete=models.CASCADE, db_column='code', primary_key=True)
	# movie = models.ForeignKey(Movie, related_name='score', on_delete=models.CASCADE, db_column='movie')
	movie = models.OneToOneField(Movie, related_name='score', on_delete=models.CASCADE, db_column='movie', verbose_name='영화')
	score_npro = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='네티즌평점')
	score_pro = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='전문가평점')
	score_m = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='남자평점')
	score_w = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='여자평점')
	score_10 = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='10대평점')
	score_20 = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='20대평점')
	score_30 = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='30대평점')
	score_40 = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='40대평점')
	score_50 = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='50대평점')
	production = models.DecimalField(max_digits=5, decimal_places=2,verbose_name='연출')
	acting = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='연기')
	story = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='스토리')
	visual = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='영상미')
	ost = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='ost')
	
	def __str__(self):
		return str(self.movie)

class Comment(models.Model):
	author = models.ForeignKey(CustomUser, related_name='comment', on_delete=models.CASCADE, db_column='author', verbose_name='작성자')
	score_user = models.DecimalField(max_digits=5, decimal_places=2,verbose_name='회원평점')
	point = models.TextField(verbose_name='포인트')
	content = models.TextField(verbose_name='내용')
	create_date = models.DateTimeField(auto_now_add=True, verbose_name='작성일')
	modify_date = models.DateTimeField(null=True, blank=True, verbose_name='수정일')
	movie = models.ForeignKey(Movie, related_name='comment', on_delete=models.CASCADE, db_column='movie', verbose_name='영화')

	def __str__(self):
		return self.content