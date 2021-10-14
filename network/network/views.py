from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django import forms
from .models import User, Posts, Profiles
import json

class PostForm(forms.Form):
    body = forms.CharField(label="", widget=forms.Textarea(attrs={'placeholder': 'Speak your mind!', 'style': 'width:100%; resize:none;'}))

class FollowForm(forms.Form):
    activate = forms.IntegerField(label="", widget=forms.TextInput(attrs={'placeholder': 'Dummy Value'}))

def like(request):
    if request.method == 'POST' and request.is_ajax:
        liked_status = False
        postID = request.POST.get('postID')
        response = {}
        #Check if user already likes post.
        for user in Posts.objects.get(id=postID).liked.all():
            if request.user == user:
                liked_status = True
        #If user hasn't liked post.
        if liked_status == False:
            Posts.objects.get(id=postID).liked.add(request.user)
            Posts.objects.get(id=postID).save()
            response = {
                'id': postID,
                'new_button': f'<input type="submit" class="btn btn-primary btn-sm" value="{Posts.objects.get(id=postID).liked.all().count()} ❤️">'
            }
        #If user already liked post.
        else:
            Posts.objects.get(id=postID).liked.remove(request.user)
            Posts.objects.get(id=postID).save()
            response = {
                'id': postID,
                'new_button': f"<input type='submit' class='btn btn-outline-primary btn-sm' id='like-button' value='{Posts.objects.get(id=postID).liked.all().count()} 🤍'>"
            }
        return HttpResponse(
            json.dumps(response),
            content_type="application/json"
        )

def edit(request):
    if request.method == 'POST' and request.is_ajax:
        postID = request.POST.get('postID')
        new_body = request.POST.get('new_body')
        this_post = Posts.objects.get(id=postID)
        this_post.body = new_body
        this_post.save()

        response = {}
        response = {
            'id': postID,
            'new_body': new_body
        }
        return HttpResponse(
            json.dumps(response),
            content_type="application/json",
        )

def index(request):
    paginator = Paginator(Posts.objects.all().order_by("datetimestamp").reverse(), 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    page_list = []
    for x in range(paginator.num_pages):
        page_list.append(x)
    if request.method == "POST":
        postform = PostForm(request.POST)
        #For new posts.
        if postform.is_valid():
            newPost = Posts(user=request.user, body=postform.cleaned_data["body"])
            newPost.save()
            Profiles.objects.get(user=request.user).posts.add(newPost)
            Profiles.objects.get(user=request.user).save()
    return render(request, "network/index.html", {
        "Post_Form": PostForm(),
        "All_Posts": Posts.objects.all(),
        "This_User": request.user,
        "page_obj": page_obj,
        "Page_List": page_list
        })

def feed(request):
    #Generate user's feed based on folow list.
    feed_list = []
    for post in Posts.objects.all().order_by("datetimestamp").reverse():
        for user in post.user.profiles.followers.all():
            if user == request.user:
                feed_list.append(post)
    paginator = Paginator(feed_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    page_list = []
    for x in range(paginator.num_pages):
        page_list.append(x)
    if request.method == "POST":
        liked_status = False
        postform = PostForm(request.POST)
        #For new posts.
        if postform.is_valid():
            newPost = Posts(user=request.user, body=postform.cleaned_data["body"])
            newPost.save()
            Profiles.objects.get(user=request.user).posts.add(newPost)
            Profiles.objects.get(user=request.user).save()
        #For likes/unlikes.
        else:
            #Check if user already likes post.
            postID = request.POST.get('postID')
            for user in Posts.objects.get(id=postID).liked.all():
                if request.user == user:
                    liked_status = True
            #If user hasn't liked post.
            if liked_status == False:
                Posts.objects.get(id=postID).liked.add(request.user)
                Posts.objects.get(id=postID).save()
            #If user already liked post.
            else:
                Posts.objects.get(id=postID).liked.remove(request.user)
                Posts.objects.get(id=postID).save()

    return render(request, "network/feed.html", {
        "Post_Form": PostForm(),
        "All_Posts": Posts.objects.all(),
        "This_User": request.user,
        "Feed_List": feed_list,
        "page_obj": page_obj,
        "Page_List": page_list
        })

def profile(request, id):
    followed_status = False
    liked_status = False
    followform = FollowForm(request.POST)
    this_profile = Profiles.objects.get(pk=id)
    paginator = Paginator(this_profile.posts.all().order_by("datetimestamp").reverse(), 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    page_list = []
    for x in range(paginator.num_pages):
        page_list.append(x)
    #Check if user already follows profile.
    for user in Profiles.objects.get(pk=id).followers.all():
        if request.user == user:
            followed_status = True

    if request.method == "POST":
        #For following/unfollowing.
        if followform.is_valid():
            if followed_status:
                Profiles.objects.get(pk=id).followers.remove(request.user)
                Profiles.objects.get(pk=id).save()
                followed_status = False
            else:
                Profiles.objects.get(pk=id).followers.add(request.user)
                Profiles.objects.get(pk=id).save()
                followed_status = True
        #For liking/unliking.
        else:
            #Check if user already likes post.
            postID = request.POST.get('postID')
            for user in Posts.objects.get(id=postID).liked.all():
                if request.user == user:
                    liked_status = True
            #If user hasn't liked post.
            if liked_status == False:
                Posts.objects.get(id=postID).liked.add(request.user)
                Posts.objects.get(id=postID).save()
            #If user already liked post.
            else:
                Posts.objects.get(id=postID).liked.remove(request.user)
                Posts.objects.get(id=postID).save()

    #Direct to profile page.
    return render(request, "network/profile.html", {
        "This_User": request.user,
        "Profile_User": this_profile.user,
        "This_Profile": this_profile,
        "This_Profile_Followers": this_profile.followers.all(),
        "This_Profile_Following": this_profile.user.follow_list.all(),
        "This_Profile_Posts": this_profile.posts.all(),
        "Follow_Form": FollowForm(initial={'activate': 1}),
        "Followed_Status": followed_status,
        "page_obj": page_obj,
        "Page_List": page_list
        })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            newProfile = Profiles(user=user)
            newProfile.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
