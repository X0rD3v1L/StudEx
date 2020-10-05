from django.db import models
from django.contrib.auth.models import User
class BookUpload(models.Model):
	title = models.CharField(max_length=30)
	author = models.ForeignKey(User,on_delete=models.CASCADE)
	file = models.FileField(upload_to="books/pdfs")
	cover = models.ImageField(upload_to='books/covers/', null=True, blank=True,default="books/covers/default.jpg")
	date_posted = models.DateTimeField(auto_now_add=True)
