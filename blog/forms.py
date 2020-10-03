from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout,Submit
from .models import BookUpload
class PlayListForm(forms.Form):
	Youtube_Playlist_Link = forms.URLField()

class SearchForm(forms.Form):
	search_word = forms.CharField()

class PocketForm(forms.Form):
	search_url = forms.URLField()

class BookUploadForm(forms.ModelForm):
	class Meta:
		model = BookUpload
		fields = ["title","book"]