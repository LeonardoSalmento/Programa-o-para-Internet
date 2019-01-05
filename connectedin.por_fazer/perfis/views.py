from django.shortcuts import render
from perfis.models import Perfil, Convite
from django.shortcuts import redirect
from perfis.forms import *
from django.contrib.auth.decorators import login_required
from django.views.generic.base import View

# Create your views here.

@login_required
def index(request):
	form = PostForm()
	perfil_logado = Perfil.objects.get(id=request.user.id)
	perfis_nao_bloqueados = perfil_logado.contatos_nao_bloqueados
	posts = Postagem.objects.all().order_by('data_publicacao')

	return render(request, 'index.html',{'perfis' : perfis_nao_bloqueados,
										 'perfil_logado' : get_perfil_logado(request),
										  'posts': posts,
										   'form':form})

@login_required
def exibir_perfil(request, perfil_id):

	perfil = Perfil.objects.get(id=perfil_id)
	is_contatos = get_perfil_logado(request).contatos.filter(id=perfil.id).exists()
	return render(request, 'perfil.html',
		          {'perfil' : perfil, 
				   'perfil_logado' : get_perfil_logado(request)})

@login_required
def convidar(request,perfil_id):

	perfil_a_convidar = Perfil.objects.get(id=perfil_id)
	perfil_logado = get_perfil_logado(request)
	
	if(perfil_logado.pode_convidar(perfil_a_convidar)):
		perfil_logado.convidar(perfil_a_convidar)
	
	return  redirect('index')


@login_required
def desfazer(request,perfil_id):
	perfil_logado = get_perfil_logado(request)	
	perfil_logado.desfazer_amizade(perfil_id)

	return  redirect('index')


@login_required
def get_perfil_logado(request):	
	return request.user.perfil

@login_required
def aceitar(request, convite_id):
	convite = Convite.objects.get(id = convite_id)
	convite.aceitar()
	return redirect('index')


@login_required
def recusar(request, convite_id):
	convite = Convite.objects.get(id = convite_id)
	convite.recusar()
	return redirect('index')

@login_required
def redefinir_senha(request):
	perfil_logado = get_perfil_logado(request)
	perfil_logado.redefinir_senha()

@login_required
def setarSuperUsuario(request, perfil_id):
	perfil = Perfil.objects.get(id = perfil_id)
	perfil.usuario.is_superuser = True
	perfil.usuario.save()
	perfil.save()
	
	return redirect('index')


@login_required
def bloquear(request, perfil_id):
	perfil_logado = get_perfil_logado(request)
	perfil_logado.bloquear_contatos(perfil_id)
	return redirect('index')


@login_required
def desbloquear(request, perfil_id):
	perfil_logado = get_perfil_logado(request)
	perfil_logado.desbloquear(perfil_id)
	return redirect('index')

@login_required
def deletar_postagem(request, postagem_id):
	postagem = Postagem.objects.get(id=postagem_id)
	postagem.excluir_postagem()

	return redirect('index')


class PostarView(View):
	def post(self, request):
		form = PostForm(request.POST)
		print(form.is_valid())
		if form.is_valid():
			dados_form = form.cleaned_data
			postagem = Postagem()
			postagem.dono = get_perfil_logado(request)
			postagem.texto = dados_form['texto']
			postagem.save()
			return redirect('index')

		return redirect('index')



#*def list_posts(request):
# 	posts = Postagem.objects.all().order_by('data_publicacao')
# 	return render(request, 'index.html', {'posts': posts})

