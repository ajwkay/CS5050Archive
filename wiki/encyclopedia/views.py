from django.shortcuts import render
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.http import HttpResponse
import markdown2
import random

from . import util

class SearchForm(forms.Form):
    search = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Search Encyclopedia'}))

class PageEdit(forms.Form):
    title = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Title'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Content Body (Please use Markdown formatting)'}), label="")

def foundInEntries(query):
    for entry in util.list_entries():
        if query.lower() == entry.lower():
            return entry
    return None

def searchResults(query):
    results = []
    for entry in util.list_entries():
        if query.lower() == entry[0:len(query)].lower():
            results.append(entry)
    return results

def index(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data["search"]
            if foundInEntries(query):
                return render(request, "encyclopedia/page.html", {
                    "entryTitle": query,
                    "entries": markdown2.markdown(util.get_entry(query)),
                    "form": SearchForm(),
                    "randomArticle": random.choice(util.list_entries())
                })
            else:
                return render(request, "encyclopedia/results.html", {
                    "query": query,
                    "results": searchResults(query),
                    "form": SearchForm(),
                    "randomArticle": random.choice(util.list_entries())
                })

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form" : SearchForm(),
        "randomArticle": random.choice(util.list_entries())
    })

def results(request):
    return render(request, "encyclopedia/results.html", {
        "entries": util.list_entries(),
        "form" : SearchForm(),
        "randomArticle": random.choice(util.list_entries())
        })

def page(request, name):
    if request.method == "POST":
        title = name
        content = util.get_entry(name)
        return render(request, "encyclopedia/pageEdit.html", {
            "form": SearchForm(),
            "pageEdit": PageEdit(initial={'title': title, 'content': content}),
            "header": title,
            "body": content,
            "randomArticle": random.choice(util.list_entries())
        })

    return render(request, "encyclopedia/page.html", {
        "entryTitle": name,
        "entries": markdown2.markdown(util.get_entry(name)),
        "form": SearchForm(),
        "randomArticle": random.choice(util.list_entries())
    })

def pageEdit(request):
    if request.method == "POST":
        form = PageEdit(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
        return render(request, "encyclopedia/page.html", {
            "entryTitle": title,
            "entries": markdown2.markdown(util.get_entry(title)),
            "form" : SearchForm(),
            "randomArticle": random.choice(util.list_entries())
            })
    return render(request, "encyclopedia/pageEdit.html", {
        "form": SearchForm(),
        "pageEdit": PageEdit(),
        "title": None,
        "content": None,
        "randomArticle": random.choice(util.list_entries())
    })
