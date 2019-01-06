from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# class Perfil(models.Model):
#     nome = models.CharField(max_length=255, null=False)
#     telefone = models.CharField(max_length=20, null= False)
#     nome_empresa = models.CharField(max_length=255, null=False)
#     email = models.CharField(max_length=255, null=False)
#     contatos = models.ManyToManyField('Perfil')

class Perfil(models.Model):
    nome = models.CharField(max_length=255, null=False)
    telefone = models.CharField(max_length=15, null=False)
    nome_empresa = models.CharField(max_length=255, null=False)
    contatos = models.ManyToManyField('self', related_name = 'meus_contatos')
    contatos_bloqueados = models.ManyToManyField('self', related_name = 'meus_contatos_bloqueados')
    usuario = models.OneToOneField(User, related_name="perfil", on_delete = models.CASCADE)
    
    @property
    def email(self):
        return self.usuario.email

    @property
    def superuser(self):
        return self.usuario.is_superuser
    
    def contatos_nao_bloqueados(self):
        perfis_nao_bloqueados = []
        
        for i in Perfil.objects.all():
            if i not in self.contatos_bloqueados.all():
                perfis_nao_bloqueados.append(i)
        return perfis_nao_bloqueados

    @property
    def get_postagens(self):
        return Postagem.objects.filter(id=self.id)
            

    def __str__(self):
        return self.nome

    def desfazer_amizade(self, perfil_id):
        self.contatos.remove(perfil_id)
        

    def convidar(self, perfil_convidado):
        if self.pode_convidar(perfil_convidado):
            convite = Convite(solicitante=self,convidado = perfil_convidado)
            convite.save()  

    def pode_convidar(self, perfil_convidado):
        return self.id != perfil_convidado.id and perfil_convidado not in self.contatos.all()


    def bloquear_contatos(self, perfil_id):
        perfil = Perfil.objects.get(id=perfil_id)
        self.contatos_bloqueados.add(perfil)

    def desbloquear(self, perfil_id):
        self.contatos_bloqueados.remove(perfil_id)   


    @property    
    def timeline(self):
        lista_postagens = []

        postagens_ordenadas = Postagem.objects.all().order_by('data_publicacao')
        for i in postagens_ordenadas:
            if i.dono in self.contatos.all() or i.dono.id == self.id:
                lista_postagens.append(i)
        
        return lista_postagens
    


class Convite(models.Model):
    solicitante = models.ForeignKey(Perfil,on_delete=models.CASCADE,related_name='convites_feitos' )
    convidado = models.ForeignKey(Perfil, on_delete= models.CASCADE, related_name='convites_recebidos')

    def aceitar(self):        
        self.solicitante.contatos.add(self.convidado)
        self.convidado.contatos.add(self.solicitante)
        self.delete()

    def recusar(self):
        self.delete()


class Postagem(models.Model):
    dono = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='minhas_postagens')

    texto = models.CharField(max_length=400, null=False)
    data_publicacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.texto

    def excluir_postagem(self):
        self.delete()