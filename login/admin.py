from django.contrib import admin
from django.contrib.auth.models import User, Group
from .models import User as MyUser

# Register your models here.
class MyUserAdmin(admin.ModelAdmin):
    fields = ["user_name"]
    # fieldsets = [
    #     ("Question", {"fields": ["question_text"]}),
    #     ("Publication Date", {"fields": ["question_pub_date"]})
    #     ]

    # inlines = [ChoiceInline]

    list_display = ["user_username", "user_name", "user_email"]
    # list_filter = ["question_pub_date"]
    # search_fields = ["question_text"]


admin.site.unregister(User)
admin.site.unregister(Group)

admin.site.register(MyUser, MyUserAdmin)


admin.AdminSite.site_header = "Kwizz"
admin.AdminSite.index_title = "Kwizz"
admin.AdminSite.site_title = "Admin"