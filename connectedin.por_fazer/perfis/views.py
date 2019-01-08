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
	perfil_logado = Perfil.objects.get(id=request.user.perfil.id)
	perfis_nao_bloqueados = perfil_logado.contatos_nao_bloqueados

	return render(request, 'index.html',{'perfis' : perfis_nao_bloqueados,
										 'perfil_logado' : get_perfil_logado(request),
										   'form':form})


@login_required
def exibir_perfil(request, perfil_id):
	form = PesquisaUsuarioForm()
	perfil = Perfil.objects.get(id=perfil_id)
	return render(request, 'perfil.html',
		          {'perfil' : perfil, 
				   'perfil_logado' : get_perfil_logado(request), 'form':form})


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
def desbloquear(request, bloqueio_id):
	bloqueio = Bloqueio.objects.get(id = bloqueio_id)
	bloqueio.desbloquear()
	return redirect('index')


@login_required
def deletar_postagem(request, postagem_id):
	postagem = Postagem.objects.get(id=postagem_id)
	postagem.excluir_postagem()

	return redirect('index')


class PostarView(View):
	def post(self, request):
		form = PostForm(request.POST)
		if form.is_valid():
			dados_form = form.cleaned_data
			postagem = Postagem()
			postagem.dono = get_perfil_logado(request)
			postagem.texto = dados_form['texto']
			postagem.save()
			return redirect('index')

		return redirect('index')


class PesquisarPerfilView(View):
	def post(self, request):
		form = PesquisaUsuarioForm(request.POST)

		if form.is_valid():
			dados_form = form.cleaned_data
			perfil_logado = get_perfil_logado(request)
			perfis_acessiveis = []
			perfis = Perfil.objects.filter(nome__icontains=dados_form['nome'])

			for perfil in perfis:
				
				if perfil_logado not in perfil.contatos_bloqueados.all():
					perfis_acessiveis.append(perfil)
			
			return render(request, 'pesquisa.html', {'perfis': perfis_acessiveis, 'perfil_logado':get_perfil_logado(request)})

		return redirect('index')
