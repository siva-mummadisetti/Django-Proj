from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse
import datetime #to get current time using datetime class and now()
import pytz # for timezone() that is passed to now() def with parameter to get current time based on time zone

from .models import *


def index(request):
    ads = Listing.objects.all()
    max_bid_list = []
    if len(ads) > 0:
        for x in ads:
            temp = x.bid.all()
            if len(temp)>0:
                temp1 = []; [temp1.append(y.quote) for y in temp]
                max_bid = max(temp1)
            else:
                max_bid = x.price # max_bid has scope outside of else block also
            max_bid_list.append(max_bid)
        ads = zip(ads, max_bid_list)
            
    return render(request, "auctions/index.html",{
        "ads" : ads
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
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        except ValueError:
            return render(request, "auctions/register.html", {
                "message": "Please fill all the fields."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def cat(request, cat):
    ads = Listing.objects.filter(category = cat)
    max_bid_list = []
    if len(ads) > 0:
        for x in ads:
            temp = x.bid.all()
            if len(temp)>0:
                temp1 = []; [temp1.append(y.quote) for y in temp]
                max_bid = max(temp1)
            else:
                max_bid = x.price # max_bid has scope outside of else block also
            max_bid_list.append(max_bid)
        ads = zip(ads, max_bid_list)
        return render(request, "auctions/index.html",{
        "ads" : ads
        })
    else:
        return render(request, "auctions/category.html",{
            "message_category" : "No results found in that category"
        })

def category(request):
    return render(request,"auctions/category.html")

def create_listing(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            title = request.POST["title"]
            description = request.POST["description"]
            img_url = request.POST["img_url"]
            category = request.POST["category"]
            price = request.POST["price"]
            if (len(title)>0 and len(description)>0 and len(img_url)>0):
                if ( len(title)<=54 and len(description)<=155):
                    try:
                        a = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
                        temp = f"{a.day}-{a.month}-{a.year}, {a.hour}:{a.minute}"
                        Listing(ad_title=title, description=description, img_url=img_url, category=category, price=price, user=request.user, time=temp).save()
                        return HttpResponseRedirect(reverse("index"))
                    except ValueError:
                        return render(request, "auctions/create_listing.html",{
                            "message":"Price field must be an integer"
                        })
                else:
                    return render(request, "auctions/create_listing.html",{
                            "message":"Error: The Number of Characters allowed for each field 👉 title - 54; description - 155"
                        })
            else:
                return render(request, "auctions/create_listing.html",{
                            "message": "Error: Please fill all the fields"
                        })
        else:
            return render(request, "auctions/login.html",{
                "message":"Please login to continue"
            })
    return render(request, "auctions/create_listing.html")

def listing(request, id):
    if request.method == "POST":
        if request.user.is_authenticated:
            temp1 = Listing.objects.get(id=id)
            temp2 = request.user.watchlist.all()
            temp3 = temp1.comment.all()
            temp4 = temp1.bid.all()
            temp5 = []; [temp5.append(x.quote) for x in temp4]
            max_bid = temp1.price
            bidder = "None"
            if len(temp5)>0:
                max_bid=max(temp5)
            if max_bid != temp1.price:
                try:
                    bidder = temp4.get(quote = max_bid).user
                except Exception:
                    return HttpResponseRedirect(reverse("listing",args = (id,) ) )
            if request.POST.get("comment_submit", False) == "post":# we can also access POST dictionary key vals via get(), here 1st arg is key of dict & 2nd is Bool value False which tells don't send default value. In some cases 1 key have 2 vals (default, user given val) on that case if key accessed give MultipleDictValError. Only get() is used to get out from that.  
                # EX a["abc"] = [1, 2, "bob"], using get() is good practise to skip defalut value
                if ((len(request.POST["comment"])>0) and (len(request.POST["comment"])<=500)):
                    a = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
                    time = f"{a.day}-{a.month}-{a.year}, {a.hour}:{a.minute}"
                    Comment(text=request.POST["comment"], user=request.user, listing=temp1, time=time).save()
                    return render(request, "auctions/listing.html",{
                    "ad":temp1,
                    "watch":temp2,
                    "comments":temp1.comment.all(),
                    "max_bid" : max_bid,
                    "bidder" : bidder
                    })
                else:
                    return render(request, "auctions/listing.html",{
                    "ad":temp1,
                    "watch":temp2,
                    "comments":temp3,
                    "max_bid" : max_bid,
                    "bidder" : bidder,
                    "message_comment":"info: you cannot post blank and 500 chars are allowed for a comment"
                    })
            if request.POST.get("bid_submit", False) == "bid":
                bid = request.POST.get("bid", False)
                if bid == "":
                    bid = 0
                else:
                    bid = int(bid)
                if ((bid > temp1.price) and (bid > max_bid)): # max() gives error if passsed empty []
                    max_bid=bid
                    Bid(quote=bid, user= request.user, listing=temp1).save()
                    try:
                        bidder = temp4.get(quote = max_bid).user
                    except Exception:
                        return HttpResponseRedirect(reverse("listing",args = (id,) ) )
                    return render(request, "auctions/listing.html",{
                    "ad":temp1,
                    "watch":temp2,
                    "comments":temp3,
                    "max_bid" : max_bid,
                    "bidder" : bidder
                    })
                else:
                    return render(request, "auctions/listing.html",{
                    "ad":temp1,
                    "watch":temp2,
                    "comments":temp3,
                    "max_bid" : max_bid,
                    "bidder" : bidder,
                    "message_bid" : "Please place the bid that is bigger than existing bids..."
                    })
            if request.POST.get("ad_flag_submit", False) == "close listing":
                temp1.flag = False
                temp1.save()
                return render(request, "auctions/listing.html",{
                "ad":temp1,
                "watch":temp2,
                "comments":temp3,
                "max_bid" : max_bid,
                "bidder" : bidder
                })
            if request.POST.get("ad_flag_submit", False) == "reopen listing":
                temp1.flag = True
                temp1.save()
                return render(request, "auctions/listing.html",{
                "ad":temp1,
                "watch":temp2,
                "comments":temp3,
                "max_bid" : max_bid,
                "bidder" : bidder
                })
        else:
            return render(request,"auctions/login.html",{
                "message":"Please login to continue"
            })
    try:
        temp1 = Listing.objects.get(id=id) # The variable declared inside if, for and try can be accessed outside of the respective blocks
    except Exception:
        raise Http404("The Requested AD is removed from our server...")  #Executed when the get() finds nothing, or more than one thing
    if request.user.is_authenticated:
        temp2 = request.user.watchlist.all()
    else:
        temp2 = []
    temp3 = temp1.comment.all()
    temp4 = temp1.bid.all()
    temp5 = []; [temp5.append(x.quote) for x in temp4]
    max_bid = temp1.price
    bidder = "None"
    if len(temp5)>0:
        max_bid=max(temp5)
    if max_bid != temp1.price:
        try:
            bidder = temp4.get(quote = max_bid).user
        except Exception:
            return HttpResponseRedirect(reverse("listing",args = (id,) ) )
    return render(request, "auctions/listing.html",{
        "ad":temp1,
        "watch":temp2,
        "comments":temp3,
        "max_bid" : max_bid,
        "bidder":bidder
    })

def list(request, id):
    if request.method == "POST":
        if request.user.is_authenticated:
            temp1 = Listing.objects.get(id=id)
            temp2 = request.user.watchlist
            if request.POST["watch"] == "watchlist":
                temp2.add(temp1)    # adding listing obj to the watchlist field
                ads = temp2.all()
                max_bid_list = []
                if len(ads) > 0:
                    for x in ads:
                        temp = x.bid.all()
                        if len(temp)>0:
                            temp1 = []; [temp1.append(y.quote) for y in temp]
                            max_bid = max(temp1)
                        else:
                            max_bid = x.price # max_bid has scope outside of else block also
                        max_bid_list.append(max_bid)
                    ads = zip(ads, max_bid_list)
                return render(request, "auctions/watchlist.html",{
                    "watchlist" : ads
                })
            if request.POST["watch"] == "unwatch":
                temp2.remove(temp1) # removing from watchlist field of User model
                return HttpResponseRedirect(reverse("listing", args=(id,)))
        else:
            return render(request,"auctions/login.html",{
                "message":"Please login to continue"
            })
def watchlist(request):
    if request.user.is_authenticated:
        ads = request.user.watchlist.all()
        max_bid_list = []
        if len(ads) > 0:
            for x in ads:
                temp = x.bid.all()
                if len(temp)>0:
                    temp1 = []; [temp1.append(y.quote) for y in temp]
                    max_bid = max(temp1)
                else:
                    max_bid = x.price # max_bid has scope outside of else block also
                max_bid_list.append(max_bid)
        ads = zip(ads, max_bid_list)
        return render(request, "auctions/watchlist.html",{
                    "watchlist" : ads
                })
    else:
        return render(request,"auctions/login.html",{
                "message":"Please login to continue"
            })
