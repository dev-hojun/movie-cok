from .models import Comment
from django import forms

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ['score_user', 'point', 'content']
		labels = {
			'score_user': '회원평점',
			'point': '포인트',
			'content': '내용',
		}