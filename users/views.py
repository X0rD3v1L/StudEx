from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm , UserUpdateForm , ProfileUpdateForm , UserLoginForm
from django.contrib.auth import authenticate, login, logout
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from notifications.models import Notification
from .tokens import account_activation_token
from django.contrib.auth.models import User
import re
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
       	n = Notification.objects.create(user = user, message =f"{user} has registerd.")
        return render(request,"users/message.html",{"message":'Thank you for your email confirmation. Now you can login your account.',"login":True})
    else:
    	return render(request,"users/message.html",{"message":'Activation link is invalid!'})
def register(request):
	if request.method == "POST":
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			email_format = re.compile(r'^(N)(\d{6})(@rguktn.ac.in)')
			if re.search(email_format , form.cleaned_data.get("email").strip()):
				user = form.save()
				current_site = get_current_site(request)
				mail_subject = 'Activate your blog account.'
				message = render_to_string('users/acc_active_email.html', {
	                'user': user,
	                'domain': current_site.domain,
	                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
	                'token':account_activation_token.make_token(user),
	            })
				to_email = form.cleaned_data.get('email')
				email = EmailMessage(
	                        mail_subject, message, to=[to_email]
	            )
				email.send()
				return render(request,"users/message.html",{"message":'Please confirm your email address to complete the registration'})
			else:
				messages.warning(request,f"Please provide your collage mail")
	else:
		form = UserRegisterForm()
	return render(request,"users/register.html",{"form":form})
@login_required
def profile(request):
	if request.method == "POST":
		u_form = UserUpdateForm(request.POST,instance=request.user)
		p_form = ProfileUpdateForm(request.POST,request.FILES , instance=request.user.profile)
		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
	else:
		u_form = UserUpdateForm(instance=request.user)
		p_form = ProfileUpdateForm(instance=request.user.profile)

	return render(request,"users/profile.html",{"u_form":u_form,"p_form":p_form})

def Login(request):
	if request.method == "POST":
		form = UserLoginForm(request.POST)
		if form.is_valid() :
			username = request.POST["username"]
			password = request.POST["password"]
			user = authenticate(username = username,password = password)
			if user is not None:
				login(request,user)
				messages.success(request,"login successfully")
				# notes = Notification.objects.all()
				# for n in notes:
				# 	if "is logged in" in n.message:
						# n.delete()
				n = Notification.objects.create(user = request.user, message = f"is logged in.")
				n.save()
				return redirect("blog-home")
			else:
				messages.error(request,"Invalid Credintials")
	else:
		form = UserLoginForm()
	return render(request,"users/login.html",{"form":form})

def Logout(request):
	messages.success(request,"logout successfully")
	# notes = Notification.objects.all()
	# for n in notes:
	# 	if "is logged out" in n.message:
	# 		n.delete()
	# 		print(n.message)
	try:
		n = Notification.objects.create(user = request.user, message = f"is logged out.")
		n.save()
	except:
		pass
	logout(request)
	return render(request,"users/logout.html")