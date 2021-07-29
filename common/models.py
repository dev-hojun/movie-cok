from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
	GENDERS = ( ('M','M'),('W','W') )
	gender=models.CharField(null=True, blank=True, max_length=1, verbose_name='성별', choices=GENDERS)
	AGES = ( ('10','10'),('20', '20'),('30', '30'),('40', '40'),('50', '50') )
	age=models.TextField(null=True, blank=True, verbose_name='연령대', choices=AGES)