from audioop import reverse
from itertools import chain
import re
from django.shortcuts import render , redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import authenticate
from . models import Comment, FollowesCount, Like, Post, Profile
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def index(request):
    user_object = User.objects.get(username = request.user)
    user_profile = Profile.objects.get(username = user_object)
    posts = Post.objects.all()

    following_list = []
    feed_list = []
    people_followed = FollowesCount.objects.filter(follower = request.user)
    for user in people_followed:
        following_list.append(user.user)
    
    for each in following_list:
        posts = Post.objects.filter(user = each)
        feed_list.append(posts)

    feed_list = chain(*feed_list)
    context = {
        'profile':user_profile ,
        'posts':feed_list
    }
    return render(request,'index.html',context)


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email = email).exists():
                messages.info(request,"Email Taken!")
                return redirect('core:signup')
            elif User.objects.filter(username = username).exists():
                messages.info (request,"Username Taken!")
                return redirect('core:signup')
            else:
                user = User.objects.create(username=username,email=email,password=password)
                user.save()
                user_object = User.objects.get(username = username)
                user_profile = Profile.objects.create(username = user_object , user_id = user_object.id)
                user_profile.save()
                return redirect('core:index')
                
                    
        else:
            messages.info(request,"Passwords are not the same")
            return redirect('core:signup')
            
    else:
        return render(request,'signup.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,"Invalid Credentials!")
            return redirect('core:signin')
    else:
        return render(request,'signin.html')


def logout(request):
    auth.logout(request)
    return redirect('core:signin')

@login_required
def settings(request):

    user_profile = Profile.objects.get(username = request.user)
    if request.method == 'POST':
        if request.FILES.get('image') == None:
            image = user_profile.profile_img
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profile_img = image
            user_profile.biography = bio
            user_profile.location = location 
            user_profile.save()
        else:
            if request.FILES.get('image') != None:
                image = request.FILES.get('image')
                bio = request.POST['bio']
                location = request.POST['location']

            user_profile.profile_img = image
            user_profile.biography = bio
            user_profile.location = location 
            user_profile.save()
   
    return render(request,'setting.html',{'user_profile':user_profile})


def upload(request):
    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']
        new_post = Post.objects.create(user=user,image=image,caption=caption)
        new_post.save()
        return redirect('/')
    else:
        return redirect('/')

def like_post(request , pk):
    username = request.user.username 
    post_id = pk
    post = Post.objects.get(id = post_id)
    like_filter = Like.objects.filter(post_id=post_id,username=username)

    if like_filter.exists():
        like_filter.delete()
        post.no_likes -= 1
        post.save()
        return redirect('/')
    else:
        new_like = Like.objects.create(post_id=post_id,username=username)
        new_like.save()
        post.no_likes += 1
        post.save()
        return redirect('/')



    
def profile(request,pk):
    user_object = User.objects.get(username = pk)
    user_profile = Profile.objects.get(username = user_object)
    user_post = Post.objects.filter(user=pk)
    post_lenght = len(user_post)
    context = {
        'user_object':user_object,
        'user_profile':user_profile,
        'user_post':user_post,
        'post_lenght':post_lenght
    }
    return render(request,'profile.html',context)


def follow(request):
    if request.method == 'POST':   
        user = request.POST['user']
        follower = request.POST['follower']
        if FollowesCount.objects.filter(follower=follower,user=user).exists():
            followed = FollowesCount.objects.get(follower=follower,user=user)
            followed.delete()      

            following_update = Profile.objects.get(username__username=follower)
            if following_update == 0:
                    following_update == 0
            else:
                following_update.following -= 1
                following_update.save()

            increase_follower = Profile.objects.get(username__username=user)
            increase_follower.follower -= 1
            increase_follower.save()

            messages.info(request,'You unfollowed this user')
            return redirect('profile/'+ user)
        else:
            following_update = Profile.objects.get(username__username=follower)
            following_update.following += 1
            following_update.save()
            new_follower = FollowesCount.objects.create(follower=follower,user=user)
            new_follower.save()
            increase_follower = Profile.objects.get(username__username=user)
            increase_follower.follower += 1
            increase_follower.save()
            messages.info(request,'Congrats you started folllowing this user')
            return redirect('profile/'+ user)
    
    else:
        messages.info(request,"You Unfollowed This User")
        return redirect('/')

#? author of comment
#? post tnat has comment
#? post belongs to which user
#? content of comment

def comment(request):
    user_object = request.user.username
    if request.method == "POST":
        author = user_object
        user = request.POST['user']
        comment = request.POST['comment']
        id = request.POST['postid']
        post = Post.objects.get(id=id)

        new_comment = Comment.objects.create(author=author,post=post,user=user,comment=comment)
        new_comment.save()
        messages.info(request,f"You add comment for post of {user}")
        return redirect('/')

    else:
        return redirect('/')