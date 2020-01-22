import datetime
from django.db import models
from django.utils import timezone
from django.conf import settings





class Client(models.Model):

	#clientid = models.CharField(max_length=50, primary_key=True)
	clientid = models.CharField(max_length=50)
	password = models.CharField(max_length=50)
	pub_date = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.clientid

	def was_published_recently(self):
		return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class PassId(models.Model):
	passid = models.CharField(max_length=50)

	def __str__(self):
		return self.passid

class Media(models.Model):


   	#clientid = models.ForeignKey(Client, on_delete=models.CASCADE, default="1")
   	clientid = models.CharField(max_length=50, default = "1")
   	img = models.ImageField(upload_to='img/', default='')
   	video = models.FileField(upload_to='video/', default='')

      #def __init__(self, img, video):
   #   self.img = img
   #   self.author = author

   #def __str__(self):
   #   return "__str__"


   	def __str__(self):
   		return self.clientid


class FriendList(models.Model):

	clientid = models.CharField(max_length=50)
	friendid = models.CharField(max_length=50)

	def __str__(self):
		return self.clientid

class FriendAddList(models.Model):

	clientid = models.CharField(max_length=50)
	friendid = models.CharField(max_length=50)

	def __str__(self):
		return self.clientid


