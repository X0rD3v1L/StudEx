from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from PIL import Image
from django.conf import settings
from django.contrib.auth.models import User

class Profile(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE)
	image   = models.ImageField(default="default.jpg",upload_to="profile_pics")
	ID_NO 	= models.CharField(max_length=7)
	def __str__(self):
		return f'{self.user.username } Profile'

	def save(self,*args,**kwargs):
		super().save(*args,**kwargs)
		image = Image.open(self.image.path)
		image.thumbnail((300,300))
		image.save(self.image.path)
# class CustomUser(AbstractUser):
# 	ID_NO = models.CharField(max_length=7,unique=True, help_text='Enter college Id.Ex : N160509',error_messages={'unique': 'A user with that ID already exists.'},verbose_name="ID_NO",null=True)
# 	def __str__(self):
# 		return self.username
