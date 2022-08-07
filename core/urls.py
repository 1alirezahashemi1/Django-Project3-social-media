from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path("",views.index,name="index"),
    path("signup/",views.signup,name="signup"),
    path("signin/",views.signin,name="signin"),
    path("logout/",views.logout,name="logout"),
    path("settings/",views.settings,name="settings"),
    path("upload",views.upload,name="upload"),
    path("like-post/<pk>",views.like_post,name="like_post"),

]