from django.forms import ModelForm
from perfis.models import *
from django.db import models
from django import forms

class PostForm(forms.Form):
	texto = forms.CharField(required=True)


class PesquisaUsuarioForm(forms.Form):
	nome = forms.CharField(required=True)
		

class DesativarContaForm(forms.Form):
	justificativa = forms.CharField(required=True)


class AtivarContaForm(forms.Form):
	email = forms.CharField(required=True)
	senha = forms.CharField(required=True)