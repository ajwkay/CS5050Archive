from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User, Bids, Listings, Comments, Watchlist

CATEGORIES=[
    ('beauty', 'Beauty'),
    ('clothes', 'Clothes'),
    ('electronics', 'Electronics'),
    ('food', 'Food'),
    ('furniture', 'Furniture'),
    ('household', 'Household'),
    ('others', 'Others'),
]

class BidForm(forms.Form):
    bid = forms.IntegerField(label="", widget=forms.TextInput(attrs={'placeholder': 'Place New Bid'}))

class EditForm(forms.Form):
    title = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Listing Title'}))
    desc = forms.CharField(label="", widget=forms.Textarea(attrs={'placeholder': 'Listing Description'}))
    category = forms.CharField(label="Pick a category", widget=forms.Select(choices=CATEGORIES))
    img_url = forms.CharField(label="", required=False, widget=forms.TextInput(attrs={'placeholder': 'Image URL'}))
    starting_bid = forms.IntegerField(label="", widget=forms.TextInput(attrs={'placeholder': 'Starting Bid'}))
    id = forms.IntegerField(label="", required=False, widget=forms.TextInput(attrs={'placeholder': 'id'}))

class CommentForm(forms.Form):
    comment_body = forms.CharField(label="", widget=forms.Textarea(attrs={'cols': 278, 'rows': 5, 'placeholder': 'Enter a new comment!'}))

class WatchlistForm(forms.Form):
    activate = forms.IntegerField(label="", widget=forms.TextInput(attrs={'placeholder': 'Dummy Value'}))

def index(request):
    if request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            openingBid = Bids(value=request.POST["starting_bid"], user=request.user)
            openingBid.save()
            newListing = Listings(category=request.POST["category"], title=request.POST["title"], desc=request.POST["desc"], img_url=request.POST["img_url"], user=request.user, highest_bid=openingBid, open=True)
            newListing.save()
        else:
            this_listing = Listings.objects.get(pk=request.POST["id"])
            title = request.POST["title"]
            desc = request.POST["desc"]
            category = request.POST["category"]
            this_listing.title = title
            this_listing.desc = desc
            this_listing.category = category
            this_listing.save()

    return render(request, "auctions/index.html", {
        "Listings": Listings.objects.all(),
        "Watchlist": Watchlist.objects.all()
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
            if Watchlist.objects.filter(user=request.user).exists():
                pass
            else:
                new_watchlist= Watchlist(user=request.user)
                new_watchlist.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            new_watchlist= Watchlist(user=user)
            new_watchlist.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def listing(request, id):
    this_listing = Listings.objects.get(pk=id)
    warning = None
    this_user = request.user
    bid_creator = this_listing.user
    try:
        this_watchlist = Watchlist.objects.get(user=this_user)
        watchlist_listings = this_watchlist.listing.all()
    except AttributeError:
        watchlist_listings = None
    except TypeError:
        this_watchlist = None
        watchlist_listings = None
    subscribed = False
    if watchlist_listings:
        for listing in watchlist_listings:
            if this_listing == listing:
                subscribed = True
    if request.method == "POST":
        form = BidForm(request.POST)
        comment = CommentForm(request.POST)
        watchlist = WatchlistForm(request.POST)
        if form.is_valid():
            if form.cleaned_data["bid"] > this_listing.highest_bid.value:
                newBid = Bids(value=form.cleaned_data["bid"], user=request.user)
                newBid.save()
                this_listing.highest_bid = newBid
                this_listing.save()
            else:
                warning = "*Please enter a valid number higher than the existing bid.*"
        if comment.is_valid():
            new_comment = Comments(user=request.user, body=comment.cleaned_data["comment_body"])
            new_comment.save()
            this_listing.comments.add(new_comment)
            this_listing.save()
        if watchlist.is_valid():
            if subscribed:
                this_watchlist.listing.remove(this_listing)
                this_watchlist.save()
                subscribed = False
            else:
                this_watchlist.listing.add(this_listing)
                this_watchlist.save()
                subscribed = True
        return render(request, "auctions/listing.html", {
            "Listings": Listings.objects.all(),
            "This_Listing": this_listing,
            "This_User": this_user,
            "Creator": bid_creator,
            "Comments": this_listing.comments.all(),
            "Bid_Form": BidForm(),
            "warning": warning,
            "Comment_Form": CommentForm(),
            "Watchlist_Form": WatchlistForm(initial={'activate': 1}),
            "Subscribed": subscribed
        })
    else:
        this_listing = Listings.objects.get(pk=id)
        this_user = request.user
        bid_creator = this_listing.user
        try:
            this_watchlist = Watchlist.objects.get(user=this_user)
            watchlist_listings = this_watchlist.listing.all()
        except AttributeError:
            watchlist_listings = None
        except TypeError:
            this_watchlist = None
            watchlist_listings = None
        subscribed = False
        if watchlist_listings:
            for listing in watchlist_listings:
                if this_listing == listing:
                    subscribed = True
        return render(request, "auctions/listing.html", {
            "Listings": Listings.objects.all(),
            "This_Listing": this_listing,
            "This_User": this_user,
            "Creator": bid_creator,
            "Comments": this_listing.comments.all(),
            "Bid_Form": BidForm(),
            "Comment_Form": CommentForm(),
            "Watchlist_Form": WatchlistForm(initial={'activate': 1}),
            "Subscribed": subscribed
            })

def watchlist(request):
    this_watchlist = Watchlist.objects.get(user=request.user)
    try:
        these_listings = this_watchlist.listing.all()
    except AttributeError:
        these_listings = None
    return render(request, "auctions/watchlist.html", {
        "This_User": request.user,
        "This_Watchlist": this_watchlist,
        "These_Listings": these_listings
    })

def categories(request, cat):

    relevant_entries = Listings.objects.filter(category=cat)
    return render(request, "auctions/categories.html", {
        "Listings": Listings.objects.all(),
        "Relevant_Listings": relevant_entries,
        "Category": cat
    })

def categorylist(request):
    return render(request, "auctions/categorylist.html",{
        "Categories": CATEGORIES
    })

def editor(request, id):
    if request.method == "POST":
        this_listing = Listings.objects.get(pk=id)
        title = this_listing.title
        desc = this_listing.desc
        img_url = this_listing.img_url
        category = this_listing.category
        return render(request, "auctions/editor.html", {
            "This_Listing": this_listing,
            "Edit_Form": EditForm(initial={'title': title, 'desc': desc, 'img_url': img_url, 'id':id, 'category': category})
    })

def creator(request):
    return render(request, "auctions/creator.html", {
        "Edit_Form": EditForm()
})

def close(request, id):
    if request.method == "POST":
        this_listing = Listings.objects.get(pk=id)
        this_user = request.user
        bid_creator = this_listing.user
        this_listing.open = False
        this_listing.save()
        try:
            this_watchlist = Watchlist.objects.get(user=this_user)
            watchlist_listings = this_watchlist.listing.all()
        except AttributeError:
            watchlist_listings = None
        except TypeError:
            this_watchlist = None
            watchlist_listings = None
        subscribed = False
        if watchlist_listings:
            for listing in watchlist_listings:
                if this_listing == listing:
                    subscribed = True
        return render(request, "auctions/listing.html", {
            "Listings": Listings.objects.all(),
            "Comments": this_listing.comments.all(),
            "This_Listing": this_listing,
            "This_User": this_user,
            "Creator": bid_creator,
            "Bid_Form": BidForm(),
            "Comment_Form": CommentForm(),
            "Subscribed": subscribed
            })
