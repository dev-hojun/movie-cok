from .models import Survey
from django import forms

class SurveyForm(forms.ModelForm):
	class Meta:
		model = Survey
		fields = ['playtime', 'age', 'score_npro', 'score_pro', 'score_gender', 'score_age', 'production', 'acting', 'story', 'visual', 'ost']
		labels = {
			'playtime': '선호상영시간',
			'age': '선호연령등급',
			'score_npro' : '네티즌평점중요도',
			'score_pro' : '전문가평점중요도',
			'score_gender' : '같은성별평점중요도',
			'score_age' : '같은연령평점중요도',
			'production' : '연출중요도',
			'acting' : '연기중요도',
			'story' : '스토리중요도',
			'visual' : '영상미중요도',
			'ost' : 'ost중요도',
		}