from django.contrib import admin

# Register your models here.
from .models import SubjectModel , FolderModel
admin.site.register(SubjectModel)
admin.site.register(FolderModel)