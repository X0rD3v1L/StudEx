from django.shortcuts import render ,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin , UserPassesTestMixin
from django.views.generic import ListView
from django.contrib import messages
from .models import BookUpload
from .forms import BookUploadForm


@login_required
def bookupload(request):
	if request.method == "POST":
		form = BookUploadForm(request.POST,request.FILES)
		if form.is_valid():
			form.instance.author = request.user
			file = form.cleaned_data.get("file")
			file = str(file)
			if (file.endswith(".pdf") or file.endswith(".doc")):
				form.save()
				messages.success(request,f'Upload Successfully.')
				redirect('booklist')
			else:
				messages.warning(request,f'Only upload pdf , docs.')
		else:
			messages.warning(request,"Form is not valid.")
	else:
		form = BookUploadForm()
	return render(request,"library/bookupload.html",{"form":form})

class BookListView(ListView):
    model = BookUpload
    template_name = 'library/booklist.html'
    context_object_name = 'books'
    paginate_by = 2

class BookListSearchView(ListView):
	model = BookUpload
	template_name = 'library/booklistsearch.html'
	context_object_name = 'books'	
	paginate_by = 2
	def get_queryset(self):
		list = []
		user = get_object_or_404(User,username=self.kwargs.get('sesarch'))
		return Post.objects.filter(author=user).order_by("-date_posted")

@login_required
def bookdelete(request, pk):
    book = BookUpload.objects.get(pk=pk)
    if (request.user.username == book.author):
    	book.delete()
    	return redirect('booklist')
    else:
    	raise PermissionDenied()