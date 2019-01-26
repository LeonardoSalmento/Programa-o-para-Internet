from django.forms import ModelForm
from myapp.models import Post
from django.db import models
from django import forms

class PostForm(ModelForm):
	

	class Meta:
		model = Post
		fields = '__all__'
		


#		fields = ['title','text']  - exibir campos especificos
#		exclude = []	    - campos que não quero



#	def is_valid(self):




#Get mostar algo
#Post salvar algum dado
