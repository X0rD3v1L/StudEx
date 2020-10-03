from django.shortcuts import render , get_object_or_404
from django.views.generic import ListView,DetailView,UpdateView,DeleteView,CreateView
from blog.models import Post , Attendence
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin , UserPassesTestMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from notifications.models import Notification
import pandas as pd ,datetime , requests , os , re
from .forms import PlayListForm , SearchForm , PocketForm , BookUploadForm
from .details import totaltime , videos , getpocket
def home(request):
	return render(request,"blog/home.html",)

def about(request):
	return render(request,"blog/about.html",{})

class PostListView(ListView):
	model = Post
	template_name = "blog/posts.html"
	context_object_name = 'posts'
	ordering = ["-date_posted"]
	paginate_by = 5
	

class UserPostListView(ListView):
	model = Post
	template_name = "blog/user_posts.html"
	context_object_name = 'posts'
	paginate_by = 3

	def get_queryset(self):
		user = get_object_or_404(User,username=self.kwargs.get('username'))
		return Post.objects.filter(author=user).order_by("-date_posted")

class PostDetailView(DetailView):
	model = Post

class PostCreateView(LoginRequiredMixin,CreateView):
	model = Post
	fields = ["title","content"]
	template_name = "blog/post_form.html"

	def form_valid(self,form):
		form.instance.author = self.request.user
		n = Notification.objects.create(user = self.request.user , message = f"{self.request.user} created a new post.")
		n.save()
		return super().form_valid(form)
	
class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):  # post_confirm_delete.html
	model = Post
	success_url = "/"

	def test_func(self):
		post = self.get_object()
		if (post.author == self.request.user):
			messages.success(self.request, f"Your Post is Updated...!")
			return True
		return False

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
	model = Post
	fields = ["title","content"]
	template_name = "blog/post_update.html"

	def form_valid(self,form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def test_func(self):
		post = self.get_object()
		if (post.author == self.request.user):
			messages.success(self.request, f"Your Post is Updated...!")
			return True
		return False
		
@login_required
def attendence(request):
	stu = Attendence.objects.filter(student=request.user).first()
	sub = stu.subjects.split()
	total = list(map(int,stu.total_cls.split()))
	present = list(map(int,stu.present_cls.split()))
	absent = [i-j for i,j in zip(total,present)]
	presents_p = [int((j/i)*100) for i,j in zip(total,present)]
	absents_p = [int((j/i)*100) for i,j in zip(total,absent)]
	total_p = sum(presents_p)/len(presents_p)
	total_a = sum(absents_p)/len(absents_p)
	presents_list = [list(i) for i in zip(sub,presents_p)]
	absents_list = [list(i) for i in zip(sub,absents_p)]
	return render(request,"blog/attendence.html",{"presents_list":presents_list,"absents_list":absents_list,"total_p":total_p,"total_a":total_a})

def chart(request):
	return render(request,"blog/charts.html")


def notif(request):
	all_notes = Notification.objects.all().order_by("-time")
	return {"notifications":all_notes}
	
def settings(request):
	return render(request,'blog/settings.html')

def test(request):
	posts = Post.objects.all()
	return render(request,'blog/test.html',{"posts":posts})

@login_required
def timetable(request):
	# l = request.user.clas.split("-")
	Batch = "E2" #l[0]
	clas = "CSE1" #l[1]
	xls = pd.ExcelFile("/home/s0m3_7h1ng/Documents/py7h0n/django/TIME TABLE 2019-20 SEMISTER-2-TENTATIVE TIME TABLE on 4.12.2019 (1).xlsx")
	e2 = pd.read_excel(xls,Batch)
	periods = e2.loc[e2["CLASS"] == clas ].values[0][1:]
	for i in range(len(periods)):
		if pd.isna(periods[i]):
			periods[i] =  periods[i-1]
		else:
			periods[i]
	days = ["Monday","Tuesday","Wednesday","Thursday","Friday"]
	periods = list([ periods[i:i+7] for i in range(0,len(periods),7)])
	List = zip(days,periods)
	return render(request,"blog/timetable.html",{"List":List})

@login_required
def today(request):
	# l = request.user.clas.split("-")
	Batch = "E2" #l[0]
	clas = "CSE1" #l[1]
	

	time = ["9:00","10:30","12:00","1:30","2:30","4:00","5:30"]

	xls = pd.ExcelFile("/home/s0m3_7h1ng/Documents/py7h0n/django/TIME TABLE 2019-20 SEMISTER-2-TENTATIVE TIME TABLE on 4.12.2019 (1).xlsx")
	e2 = pd.read_excel(xls,Batch)
	periods = e2.loc[e2["CLASS"] == clas ].values[0][1:]
	for i in range(len(periods)):
		if pd.isna(periods[i]):
			periods[i] =  periods[i-1]
		else:
			periods[i]
	periods = list([ periods[i:i+7] for i in range(0,len(periods),7) ])
	periods = periods[datetime.datetime.today().weekday()]

	df = pd.read_csv('Teachers.csv')
	subjects = df['SUBJECT']
	sections = df['SECTIONS']
	faculty = df['NAME OF THE FACULTY']
	subj_dic = lab_dic = {}
	for fac_name,subject,section in zip(faculty,subjects,sections):
		sect = [sec for sec in section.split(',')]
		if subject not in subj_dic:
			d = {fac_name:sect}
			subj_dic[subject]= d
		else:
			subj_dic[subject][fac_name]=section
	teachers = []
	for sub in subjects:
		for fac in subj_dic[sub]:
			if clas[-1] in subj_dic[sub][fac]:
				teachers.append(fac)
	labs = df['LAB']
	lab_sections = df['SECTIONS.1']
	for fac_name,lab,section in zip(faculty,labs,lab_sections):
		if (isinstance(section,float)):
			pass
		# elif ("," in lab):
		# 	if ("." in section):
		# 		sections = str(section).split(".")
		# 		labs = lab.split(",")
		# 	else:
		# 		sections=[section,section]
		# 		labs = lab.split(",")
		# 	for lab,section in zip(labs,sections):
		# 		sect = [sec.strip() for sec in section.split(',')]
		# 		if lab not in lab_dic:
		# 			d = {fac_name:sect}
		# 			lab_dic[lab.strip()] = d
		# 		else:
		# 			lab_dic[lab.strip()][fac_name] = sect
		else:
			sect = [sec.strip() for sec in section.split(',')]
			if lab not in lab_dic:
				d = {fac_name:sect}
				lab_dic[lab.strip()] = d
			else:
				lab_dic[lab.strip()][fac_name] = sect
				
	std_atd = Attendence.objects.filter(student=request.user).first()
	subjects = std_atd.subjects.split(",")
	total_cls = list(map(int,std_atd.total_cls.split()))
	present_cls = list(map(int,std_atd.present_cls.split()))
	percentage = []
	for period in periods:
		i = subjects.index(period)
		percentage.append((present_cls[i]/total_cls[i])*100)

	status = ["S" for i in range(7)]
	
	List = list(zip(list(range(1,len(periods)+1)),time,periods,teachers,percentage,status))
	return render(request,"blog/today.html",{"List":List})



def getTime(request):
	List=""
	if request.method == 'POST':
		form = PlayListForm(request.POST)
		if form.is_valid():
			url = form.cleaned_data['Youtube_Playlist_Link']
			PlayListID = re.search(r"[?&]list=([^#\&\?]+)",url)
			times , px= totaltime(PlayListID.group(1))
			List=list(zip(times,px))
	else:
		form = PlayListForm()
	return render(request,'blog/youtube_playlist.html',{'form':form,"List":List})
def getVideos(request):
	videos_list=[]
	if request.method=="POST":
		form = SearchForm(request.POST)
		if form.is_valid():
			word = form.cleaned_data["search_word"]
			videos_list = videos(word)
	else:
		form = SearchForm()
	return render(request,"blog/youtube_search.html",{"form":form,"List":videos_list})

def pocket(request):
	if request.method == "POST":
		form = PocketForm(request.POST)
		if form.is_valid():
			url = form.cleaned_data.get("search_url")
			print(url)
			dic = getpocket(url)
	else:
		form = PocketForm()
		dic={}
	return render(request,"blog/pocket.html",{"form":form,"dic":dic})


@login_required
def analysis(request):
	files = os.listdir("media/Analysis")
	files.sort()
	return render(request,"blog/analysis.html",{"files":files})

@login_required
def bookupload(request):
	if request.method == "POST":
		form = BookUploadForm(request.POST,request.FILES)
		if form.is_valid():
			file = form.cleaned_data.get("book")
			file = str(file)
			if (file.endswith(".pdf") or file.endswith(".doc")):
				form.save()
				messages.success(request,f'Upload Successfully.')
			else:
				messages.warning(request,f'Only upload pdf , docs.')
		else:
			messages.warning(request,"form is not valid.")

	return render(request,"blog/bookupload.html",{"form":form})