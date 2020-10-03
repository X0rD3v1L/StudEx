from django.contrib import admin
from .models import Profile 
from django.contrib.auth.admin import UserAdmin
from .forms import UserRegisterForm

# class CustomUserAdmin(UserAdmin):
# 	user = CustomUser
# 	add_form = UserRegisterForm
# 	fieldsets = (
# 		*UserAdmin.fieldsets , 
# 		(
# 			"User",
# 			{
# 				"fields":(
# 					"ID_NO",
# 				)
# 			}
# 		)
# 	)
admin.site.register(Profile)
# admin.site.register(CustomUser,CustomUserAdmin)