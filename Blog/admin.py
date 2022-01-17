from django.contrib import admin

# Register your models here.
from Blog.models import CustomUser, Post


@admin.register(CustomUser)
class CustomUser(admin.ModelAdmin):
    list_display = ['name', 'email', 'mobile', 'date_joined']

    def save_model(self, request, obj, form, change):
        obj.set_password(obj.password)
        obj.save()
        super(CustomUser, self).save_model(request, obj, form, change)


# Customize the way the admin panel looks
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'posted_date_on')  # displays the properties mentioned in the tuple
    list_filter = ('posted_date_on',)
    search_fields = ['title', 'Body']


# Register your models here.
admin.site.register(Post, PostAdmin)
