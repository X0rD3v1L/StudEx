from django.db import models
from django.utils import timezone
from django.shortcuts import reverse
from django.conf import settings
# Create your models here.

class Post(models.Model):
	title 		= models.CharField(max_length=30)
	content		= models.TextField()
	date_posted	= models.DateTimeField(default=timezone.now)
	author		= models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('post-detail',kwargs={"pk":self.pk})

class Attendence(models.Model):
	student = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
	subjects = models.CharField(max_length=200)
	total_cls = models.CharField(max_length=200)
	present_cls = models.CharField(max_length=200)

class PeriodTable(models.Model):
	period = models.AutoField(primary_key = True)
	subject = models.CharField(max_length=30)
	time = models.CharField(max_length=30)
	teacher = models.CharField(max_length=30)

class BookUpload(models.Model):
	title = models.CharField(max_length=30)
	book = models.FileField(upload_to="books")
