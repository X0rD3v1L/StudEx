from django.db import models

class SubjectModel(models.Model):
	SubjectID = models.IntegerField(primary_key=True)
	SubjectName = models.CharField(max_length=200)

class FolderModel(models.Model):
	FolderID = models.IntegerField(primary_key=True)
	FolderName = models.CharField(max_length=200)
	