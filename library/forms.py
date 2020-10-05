from django import forms
from .models import BookUpload
class BookUploadForm(forms.ModelForm):
	class Meta:
		model = BookUpload
		fields = ["title","file"]
