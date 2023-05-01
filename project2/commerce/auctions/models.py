from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser): # AbstractUser is not an abstract class, it has fields implemented for username, password ....
    watchlist = models.ManyToManyField("Listing", blank = True, related_name = "watch")
    def __str__(self):
        return f"{self.username}"

class Listing(models.Model):
    ad_title = models.CharField(max_length = 54)
    description = models.CharField(max_length = 155)
    img_url = models.CharField(max_length = 2000)
    category = models.CharField(max_length = 30, blank = True)
    price = models.IntegerField()
    time = models.CharField(max_length = 20)
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "listing")
    flag = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.ad_title}"

class Bid(models.Model):
    quote = models.IntegerField()
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete = models.CASCADE, related_name = "bid")
    def __str__(self):
        return f"{self.quote}"

class Comment(models.Model):
    text = models.CharField(max_length = 500)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete = models.CASCADE, related_name = "comment")
    time = models.CharField(max_length = 20)
    def __str__(self):
        return f"{self.text}"