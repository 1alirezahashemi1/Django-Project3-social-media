from django.contrib import admin
from .models import Profile , Post , Like
# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ['id','user','created_at']
    list_filter = ['user']

admin.site.register(Post,PostAdmin)
admin.site.register(Profile)
admin.site.register(Like)