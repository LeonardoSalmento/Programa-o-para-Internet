from django.db import models

class Post(models.Model):
	title = models.CharField(max_length=1000)
	text = models.CharField(max_length=255)
	# autor = models.CharField(max_length=255)
	date_published = models.DateTimeField()

	def __str__(self):
		return self.title
