from django.http.response import Http404, HttpResponse
from django.shortcuts import render
from markdown2 import markdown
from random import choice

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki_entry(request, title):
    data = util.get_entry(title)
    try:
        inject = markdown(data)
    except TypeError:
        raise Http404("Requested Page Not Found 🙃")
    return render(request,"encyclopedia/entries.html",
    {
        "title": title.title(),
        "inject": inject
    })

def search(request):
    if request.method == 'POST':
        data = util.get_entry(request.POST["q"])
        if data != None:
            return render(request,"encyclopedia/entries.html",{
                "title" : request.POST["q"].title(),
                "inject" : markdown(data) 
            })
        else:
            query = request.POST["q"]
            if query.lower() in ("",):
                return render(request, "encyclopedia/index.html", {
                    "entries": util.list_entries()
                })
            if query.lower() in (" ","  ","   ","    "):
                return render(request, "encyclopedia/index.html", {
                "entries": util.list_entries()
                })
            temp = []
            for x in (util.list_entries()):
                if query.lower() in (x.lower()):
                    temp.append(x)
            if len(temp) > 0 :
                return render(request,"encyclopedia/search_result.html",{
                    "match" : temp,
                    "text" : "No entry exists with name",
                    "query" : query,
                    "text1" : "Some of the similar matches:"
                })
            else:
                return render(request,"encyclopedia/search_result.html",{
                    "text" : "Oops! nothing found, try again with different query 🙃<p></p>",
                    "text2": "You searched for :",
                    "query" : query
                })
    return render(request, "encyclopedia/index.html", {
                    "entries": util.list_entries()
        })
def editor(request):
    if request.method == 'POST' :
        title = request.POST["title"]
        content = request.POST["content"]
        if len(title) > 0:
            if (title.lower()) in [ x.lower() for x in (util.list_entries()) ] : # list comprehensions
                return render(request,"encyclopedia/editor.html",{
                    "text1" : "Error :",
                    "text2" : "\'Entry already exists with same title.\'",
                    "text3" : "Info : To modify entry content goto entry page"
                })
        if (len(title) <= 0) or (len(content) <= 0):
            return render(request,"encyclopedia/editor.html",{
                    "text1" : "Error :",
                    "text2" : "\'Title, Content fields of the Entry should not be empty .\'"
                })
        else:
            util.save_entry(title, content)
            return render(request,"encyclopedia/entries.html",
                {
                    "title": title,
                    "inject": markdown(util.get_entry(title))
                })            
    return render(request,"encyclopedia/editor.html")
def mod(request, title):
    if request.method == 'POST' :
        content = request.POST["content"]
        if (len(content) <= 0):
            return render(request,"encyclopedia/mod.html",{
                    "title" : title,
                    "content" : util.get_entry(title),
                    "text1" : "Error :",
                    "text2" : "\'Content fields of the Entry should not be empty .\'"
                })
        else:
            util.save_entry(title, content)
            return render(request,"encyclopedia/entries.html",{
                "title" : title,
                "inject" : markdown(util.get_entry(title))
            })
    return render(request,"encyclopedia/mod.html",{
        "title" : title,
        "content" : util.get_entry(title)
    })
def random(request):
    if len(util.list_entries()) > 0 :
        title = choice(util.list_entries())
        return render(request,"encyclopedia/entries.html",{
            "title" : title,
            "inject" : markdown(util.get_entry(title))
        })
    else:
        raise Http404("Nothing found...")