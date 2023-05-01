from django.contrib import admin

from .models import *

class UserAdmin(admin.ModelAdmin):
    list_display=("id", "username")
    filter_horizontal=("watchlist",)

class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "ad_title", "category", "price", "user","time", "flag")

class BidAdmin(admin.ModelAdmin):
    list_display=("id", "listing", "quote", "user")

class CommentAdmin(admin.ModelAdmin):
    list_display=("id", "listing", "user")

admin.site.register(User, UserAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
