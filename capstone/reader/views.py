from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator
from django.db import IntegrityError
from django.db.models import Avg, Count
from django.db.models.functions import Lower
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django import forms
from pathlib import Path
from .models import *
from uuid import uuid4
import json, os, shutil, errno, patoolib

def regenerate_unique_directory(story_item, type):
    story_item.story_folder_id=uuid4().hex
    story_item.save()
    new_dir_path = os.path.join(static_dir, f"library/{type}/{story_item.story_folder_id}")
    try:
        os.makedirs(new_dir_path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            #directory already exists
            generate_unique_directory(story_item, type)
        else:
            print(e)

def validate_hype(value):
  ext = os.path.splitext(value.name)[1]
  valid_extensions = ['.zip','.rar','.zipx','.7z']
  if not ext in valid_extensions:
    raise ValidationError('Upload a valid story file. The file must be in the format of a zipped folder.')

class CommentForm(forms.Form):
    body = forms.CharField(label="", widget=forms.Textarea(attrs={'style': 'width:100%; height: 100px; resize:none;'}))

class ReviewForm(forms.Form):
    rating = forms.TypedChoiceField(label="", choices=RATINGS, coerce=int)
    body = forms.CharField(label="", widget=forms.Textarea(attrs={'style': 'width:100%; height: 250px; resize:none;'}))

class FollowForm(forms.Form):
    activate = forms.IntegerField(label="", widget=forms.TextInput(attrs={'placeholder': 'Dummy Value'}))

class UploadForm(forms.Form):
    title = forms.CharField(label="", max_length = 80, widget=forms.TextInput(attrs={'placeholder': 'Title'}))
    genre = forms.ChoiceField(label='', choices=GENRE_TAGS)
    cover = forms.ImageField(label='Cover Photo')
    description = forms.CharField(label="", max_length = 1100, widget=forms.Textarea(attrs={'style': 'width:100%; resize:none;', 'placeholder': 'Write a short abstract for your story (max 1100 char).'}))
    story_file = forms.FileField(label='Story File', validators=[validate_hype])
    editor_used = forms.ChoiceField(label='', choices=EDITOR_USED)

def index(request, sort="", current_count=1):
    all_stories = Stories.objects.all().order_by('date_time_submitted').reverse()
    current_sort = ""
    name_count = 1
    rating_count = 1
    reviews_count = 1
    date_count = 1
    if sort == "name":
        current_sort = "name"
        rating_count = 1
        reviews_count = 1
        date_count = 1
        if current_count == 1:
            name_count = 2
            all_stories = Stories.objects.all().order_by(Lower('title'))
        elif current_count == 2:
            name_count = 1
            all_stories = Stories.objects.all().order_by(Lower('title')).reverse()
    if sort == "rating":
        current_sort = "rating"
        name_count = 1
        reviews_count = 1
        date_count = 1
        if current_count == 1:
            rating_count = 2
            all_stories = Stories.objects.all().order_by('avg_rating').reverse()
        elif current_count == 2:
            rating_count = 1
            all_stories = Stories.objects.all().order_by('avg_rating')
    if sort == "reviews":
        current_sort = "reviews"
        rating_count = 1
        name_count = 1
        date_count = 1
        if current_count == 1:
            reviews_count = 2
            all_stories = Stories.objects.all().annotate(count=Count('reviews')).order_by('count').reverse()
        elif current_count == 2:
            reviews_count = 1
            all_stories = Stories.objects.all().annotate(count=Count('reviews')).order_by('count')
    if sort == "date":
        current_sort = "date"
        rating_count = 1
        name_count = 1
        reviews_count = 1
        if current_count == 1:
            date_count = 2
            all_stories = Stories.objects.all().order_by('date_time_submitted').reverse()
        elif current_count == 2:
            date_count = 1
            all_stories = Stories.objects.all().order_by('date_time_submitted')
    return render(request, 'reader/index.html', {
        "All_Stories": all_stories,
        "Name_Count" : name_count,
        "Rating_Count" : rating_count,
        "Reviews_Count": reviews_count,
        "Date_Count": date_count,
        "Current_Sort": current_sort
    })

def profile(request, id):
    followed_status = False
    commentform = CommentForm(request.POST)
    followform = FollowForm(request.POST)
    #Check if user alredy follows profile.
    for user in Profiles.objects.get(user=User.objects.get(pk=id)).followers.all():
        if request.user == user:
            followed_status = True
            break

    #Follow/Unfollow
    if request.method == "POST":
        if followform.is_valid():
            response = {}
            if followed_status:
                Profiles.objects.get(user=User.objects.get(pk=id)).followers.remove(request.user)
                Profiles.objects.get(user=User.objects.get(pk=id)).save()
                followed_status = False
            else:
                Profiles.objects.get(user=User.objects.get(pk=id)).followers.add(request.user)
                Profiles.objects.get(user=User.objects.get(pk=id)).save()
                followed_status = True

        #Commenting
        elif commentform.is_valid():
            newComment = Comments(author=request.user, body=commentform.cleaned_data["body"], profile=Profiles.objects.get(user=User.objects.get(pk=id)))
            newComment.save()

        return render(request, "reader/profile.html", {
            "This_Profile": Profiles.objects.get(user=User.objects.get(pk=id)),
            "This_Profile_Stories": Stories.objects.filter(author=User.objects.get(pk=id)).all(),
            "Comment_Form": CommentForm(),
            "Follow_Form": FollowForm(initial={'activate': 1}),
            "Followed_Status": followed_status
        })

    #Any other redirect
    else:
        return render(request, "reader\profile.html", {
            "This_Profile": Profiles.objects.get(user=User.objects.get(pk=id)),
            "This_Profile_Stories": Stories.objects.filter(author=User.objects.get(pk=id)).all(),
            "Comment_Form": CommentForm(),
            "Follow_Form": FollowForm(initial={'activate': 1}),
            "Followed_Status": followed_status
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
            return render(request, "reader\profile.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "reader/login.html")


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
            return render(request, "reader/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            newProfile = Profiles(user=user)
            newProfile.save()
        except IntegrityError:
            return render(request, "reader/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "reader/register.html")



def story(request, id):
    if request.method == "POST":
        reviewform = ReviewForm(request.POST)
        #Reviews on Stories
        if reviewform.is_valid():
            newReview = Reviews(author=request.user, rating=reviewform.cleaned_data["rating"], body=reviewform.cleaned_data["body"], story=Stories.objects.get(story_folder_id=id))
            newReview.save()
            calculated_avg = Stories.objects.get(story_folder_id=id).reviews.all().aggregate(Avg('rating'))
            this_story = Stories.objects.get(story_folder_id=id)
            this_story.avg_rating = calculated_avg['rating__avg']
            this_story.save()

    #Check if user has reviewed the story.
    reviewed_status = False
    for review in Stories.objects.get(story_folder_id=id).reviews.all():
        if request.user == review.author:
            reviewed_status = True

    return render(request, "reader/story.html", {
        "This_Story": Stories.objects.get(story_folder_id=id),
        "Review_Form": ReviewForm(),
        "Reviewed_Status": reviewed_status
    })

def edit(request):
    if request.method == 'POST':
        reviewID = request.POST.get('reviewID')
        new_body = request.POST.get('new_body')
        new_rating = request.POST.get('new_rating')
        storyfolderID = request.POST.get('storyfolderID')
        Reviews.objects.get(id=reviewID).likes.clear()
        this_review = Reviews.objects.get(id=reviewID)
        this_review.body = new_body
        this_review.rating = new_rating
        this_review.save()
        calculated_avg = Stories.objects.get(story_folder_id=storyfolderID).reviews.all().aggregate(Avg('rating'))
        this_story = Stories.objects.get(story_folder_id=storyfolderID)
        this_story.avg_rating = calculated_avg['rating__avg']
        this_story.save()
        response = {
            'new_body': new_body,
            'new_rating': new_rating,
            'new_avg_rating': Stories.objects.get(story_folder_id=storyfolderID).avg_rating,
            'reviewID': reviewID,
            'new_button': f"<input type='submit' class='btn btn-outline-primary btn-sm' id='like-button' value='{Reviews.objects.get(id=reviewID).likes.all().count()} 🤍'>"
        }
        return HttpResponse(
            json.dumps(response),
            content_type="application/json"
        )

def like(request):
    if request.method == 'POST' and request.is_ajax:
        liked_status = False
        reviewID = request.POST.get('reviewID')
        response = {}
        #Check if user already likes review.
        for user in Reviews.objects.get(id=reviewID).likes.all():
            if request.user == user:
                liked_status = True
        #If user hasn't liked review.
        if liked_status == False:
            Reviews.objects.get(id=reviewID).likes.add(request.user)
            Reviews.objects.get(id=reviewID).save()
            response = {
                'id': reviewID,
                'new_button': f'<input type="submit" class="btn btn-primary btn-sm" value="{Reviews.objects.get(id=reviewID).likes.all().count()} ❤️">'
            }
        #If user already liked review.
        else:
            Reviews.objects.get(id=reviewID).likes.remove(request.user)
            Reviews.objects.get(id=reviewID).save()
            response = {
                'id': reviewID,
                'new_button': f"<input type='submit' class='btn btn-outline-primary btn-sm' id='like-button' value='{Reviews.objects.get(id=reviewID).likes.all().count()} 🤍'>"
            }
        return HttpResponse(
            json.dumps(response),
            content_type="application/json"
        )

def reader(request, id, type):
    if type == "HypeDyn2":
        return render(request, 'reader/reader-hypdyn2.html', {
            "Story_ID" : id
        })
    elif type == "Twine":
        return render(request, 'reader/reader-twine.html', {
            "Story_ID" : id
        })
    elif "Squiffy":
        return render(request, 'reader/reader-squiffy.html', {
            "Story_ID" : id
        })
    else:
        return render(request, 'reader/reader-twine.html', {
            "Story_ID" : id
        })

def submit(request):
    if request.method == "POST":
        uploadform = UploadForm(request.POST, request.FILES)
        #Uploading a new story.
        if uploadform.is_valid():
            newStory = Stories(
                author=request.user,
                tags=uploadform.cleaned_data["genre"],
                title=uploadform.cleaned_data["title"],
                description=uploadform.cleaned_data["description"],
                cover=request.FILES["cover"],
                editor_used=uploadform.cleaned_data["editor_used"],
                story_folder_id=uuid4().hex
            )
            newStory.save()
            #Getting static folder path from project settings
            static_dir = settings.STATICFILES_DIRS[0]

            instance = DummyModel(file_field=request.FILES["story_file"])
            instance.save()

            #Creating a folder in static directory
            new_dir_path = os.path.join(static_dir, f"library/{newStory.editor_used}/{newStory.story_folder_id}")
            try:
                os.makedirs(new_dir_path)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    #directory already exists
                    regenerate_unique_directory(newStory, uploadform.cleaned_data["editor_used"])
                    pass
                else:
                    print(e)

            #Unzipping submitted files into the newly created folder.
            patoolib.extract_archive(instance.file_field.path, outdir=new_dir_path)
            instance.delete()

            #Renaming .html file for Twine entries.
            if uploadform.cleaned_data["editor_used"] == "Twine":
                os.rename(os.path.join(new_dir_path, os.listdir(new_dir_path)[0]), os.path.join(new_dir_path, f"{newStory.story_folder_id}.html"))

            return render(request, 'reader/story.html', {
                "This_Story": Stories.objects.get(story_folder_id=newStory.story_folder_id),
                "Review_Form": ReviewForm(),
            })
        else:
            print(uploadform.errors)
            return render(request, 'reader/submit.html', {
                'Upload_Form': uploadform,
                'Errors': uploadform.errors
            })
    else:
        return render(request, 'reader/submit.html', {
            'Upload_Form': UploadForm(),
            'Errors': ""
        })

def intro_edit(request):
    if request.method == 'POST':
        profileID = request.POST.get('profile_id')
        new_intro = request.POST.get('new_intro')
        this_profile = Profiles.objects.get(pk=profileID)
        this_profile.intro = new_intro
        this_profile.save()
        response = {
            'new_intro': new_intro,
            'profile_id': profileID
        }
        return HttpResponse(
            json.dumps(response),
            content_type="application/json"
        )

def category(request, type, query):
    author_type = False
    if type == 'author':
        all_stories = Stories.objects.filter(author=User.objects.get(pk=query)).all()
        header = f"{User.objects.get(pk=query)}'s Stories"
        author_type = True
    elif type == 'genre':
        all_stories = Stories.objects.filter(tags=query).all()
        header = query
    return render(request, 'reader/category.html', {
        'All_Stories': all_stories,
        'Header': header,
        "Author_Type": author_type
    })
